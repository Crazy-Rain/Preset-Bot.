#!/usr/bin/env python3
"""
Demo script to show avatar URL validation in action
Run this to see examples of validation results
"""

import sys
from unittest.mock import MagicMock

# Mock tkinter
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.scrolledtext'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

from gui import PresetBotGUI


def demo_validation():
    """Demonstrate URL validation with various test cases"""
    
    # Create GUI instance (mocked)
    with MagicMock() as mock_root:
        gui = PresetBotGUI.__new__(PresetBotGUI)
    
    print("=" * 70)
    print("Avatar URL Validation Demo")
    print("=" * 70)
    print()
    
    # Test cases
    test_cases = [
        ("Empty URL", ""),
        ("Invalid format (no protocol)", "example.com/image.png"),
        ("Valid PNG (imgur)", "https://i.imgur.com/abc123.png"),
        ("Valid JPEG", "https://example.com/avatar.jpg"),
        ("Non-image URL", "https://example.com/page.html"),
    ]
    
    for description, url in test_cases:
        print(f"Test: {description}")
        print(f"URL: {url if url else '(empty)'}")
        
        is_valid, message = gui.validate_avatar_url(url)
        
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"Result: {status}")
        print(f"Message: {message}")
        print("-" * 70)
        print()


if __name__ == "__main__":
    demo_validation()
