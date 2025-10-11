#!/usr/bin/env python3
"""Test avatar URL validation functionality"""

import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
import requests


# Mock tkinter before importing gui
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.scrolledtext'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

# Now we can import gui
from gui import PresetBotGUI


class TestAvatarValidation(unittest.TestCase):
    """Test avatar URL validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the root window and all tkinter dependencies
        self.mock_root = MagicMock()
        
        # Create a partial mock of PresetBotGUI that only has validate_avatar_url
        with patch.object(PresetBotGUI, '__init__', lambda x, y: None):
            self.gui = PresetBotGUI(None)
    
    @patch('requests.head')
    def test_valid_url(self, mock_head):
        """Test validation of a valid URL"""
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'image/png', 'Content-Length': '100000'}
        mock_head.return_value = mock_response
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/avatar.png')
        
        self.assertTrue(is_valid)
        self.assertIn('valid', message.lower())
    
    def test_empty_url(self):
        """Test validation of empty URL"""
        is_valid, message = self.gui.validate_avatar_url('')
        
        self.assertFalse(is_valid)
        self.assertIn('empty', message.lower())
    
    def test_invalid_url_format(self):
        """Test validation of invalid URL format"""
        is_valid, message = self.gui.validate_avatar_url('not-a-valid-url')
        
        self.assertFalse(is_valid)
        self.assertIn('http', message.lower())
    
    @patch('requests.head')
    def test_url_not_found(self, mock_head):
        """Test validation of URL that returns 404"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/missing.png')
        
        self.assertFalse(is_valid)
        self.assertIn('404', message)
    
    @patch('requests.head')
    @patch('requests.get')
    def test_invalid_content_type(self, mock_get, mock_head):
        """Test validation of URL with invalid content type"""
        # Mock HEAD request with wrong content type
        mock_head_response = Mock()
        mock_head_response.status_code = 200
        mock_head_response.headers = {'Content-Type': 'text/html'}
        mock_head.return_value = mock_head_response
        
        # Mock GET request (fallback) also with wrong content type
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.headers = {'Content-Type': 'text/html'}
        mock_get.return_value = mock_get_response
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/not-image.html')
        
        self.assertFalse(is_valid)
        self.assertIn('invalid', message.lower())
    
    @patch('requests.head')
    def test_large_image_warning(self, mock_head):
        """Test validation of large image (should warn but allow)"""
        # Mock a response with large image (3MB - should warn)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'image/png', 'Content-Length': str(3 * 1024 * 1024)}
        mock_head.return_value = mock_response
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/large.png')
        
        self.assertTrue(is_valid)
        self.assertIn('⚠️', message)
        self.assertIn('large', message.lower())
    
    @patch('requests.head')
    def test_too_large_image(self, mock_head):
        """Test validation of image that's too large"""
        # Mock a response with image larger than 8MB
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'image/png', 'Content-Length': str(10 * 1024 * 1024)}
        mock_head.return_value = mock_response
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/toolarge.png')
        
        self.assertFalse(is_valid)
        self.assertIn('too large', message.lower())
    
    @patch('requests.head')
    def test_timeout(self, mock_head):
        """Test validation when request times out"""
        mock_head.side_effect = requests.exceptions.Timeout()
        
        is_valid, message = self.gui.validate_avatar_url('https://example.com/slow.png')
        
        self.assertFalse(is_valid)
        self.assertIn('timed out', message.lower())
    
    @patch('requests.head')
    def test_connection_error(self, mock_head):
        """Test validation when connection fails"""
        mock_head.side_effect = requests.exceptions.ConnectionError()
        
        is_valid, message = self.gui.validate_avatar_url('https://unreachable.com/avatar.png')
        
        self.assertFalse(is_valid)
        self.assertIn('connection', message.lower())


if __name__ == '__main__':
    unittest.main()
