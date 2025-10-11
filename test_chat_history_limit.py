#!/usr/bin/env python3
"""
Test configurable chat history limit
"""

import sys
from unittest.mock import MagicMock

# Mock discord before importing bot
sys.modules['discord'] = MagicMock()
sys.modules['discord.ext'] = MagicMock()
sys.modules['discord.ext.commands'] = MagicMock()

from bot import ConfigManager

def test_chat_history_limit():
    """Test that chat history limit can be configured"""
    
    # Create config manager
    config_manager = ConfigManager()
    
    # Test default value
    default_limit = config_manager.get_chat_history_limit()
    assert default_limit == 20, f"Default limit should be 20, got {default_limit}"
    print(f"✓ Default limit: {default_limit}")
    
    # Test setting a new value
    config_manager.set_chat_history_limit(50)
    new_limit = config_manager.get_chat_history_limit()
    assert new_limit == 50, f"Expected 50, got {new_limit}"
    print(f"✓ Set limit to 50: {new_limit}")
    
    # Test setting to 100
    config_manager.set_chat_history_limit(100)
    limit_100 = config_manager.get_chat_history_limit()
    assert limit_100 == 100, f"Expected 100, got {limit_100}"
    print(f"✓ Set limit to 100: {limit_100}")
    
    # Test minimum value (should be at least 1)
    config_manager.set_chat_history_limit(0)
    min_limit = config_manager.get_chat_history_limit()
    assert min_limit >= 1, f"Limit should be at least 1, got {min_limit}"
    print(f"✓ Minimum limit enforced: {min_limit}")
    
    # Test negative value (should be at least 1)
    config_manager.set_chat_history_limit(-5)
    neg_limit = config_manager.get_chat_history_limit()
    assert neg_limit >= 1, f"Limit should be at least 1, got {neg_limit}"
    print(f"✓ Negative value corrected: {neg_limit}")
    
    # Test string conversion
    config_manager.set_chat_history_limit("75")
    str_limit = config_manager.get_chat_history_limit()
    assert str_limit == 75, f"Expected 75, got {str_limit}"
    print(f"✓ String conversion works: {str_limit}")
    
    print("\n✓ All chat history limit tests passed!")

if __name__ == "__main__":
    print("Testing configurable chat history limit...")
    test_chat_history_limit()
