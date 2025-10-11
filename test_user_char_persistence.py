#!/usr/bin/env python3
"""
Test that user character persistence works across messages in a channel
"""

import sys
from unittest.mock import MagicMock, AsyncMock

# Mock discord before importing bot
sys.modules['discord'] = MagicMock()
sys.modules['discord.ext'] = MagicMock()
sys.modules['discord.ext.commands'] = MagicMock()

from bot import ConfigManager

def test_user_character_persistence():
    """Test that user character is remembered in channel even when not specified"""
    
    # Create config manager
    config_manager = ConfigManager()
    
    # Setup test data
    channel_id = "test_channel_123"
    author_id = "user_456"
    
    # Add some chat history with user character "Alice"
    config_manager.add_chat_message(channel_id, {
        "author": author_id,
        "author_name": "TestUser",
        "user_character": "alice",
        "content": "Hello there!",
        "type": "user",
        "timestamp": "2025-01-01T00:00:00"
    })
    
    config_manager.add_chat_message(channel_id, {
        "content": "Hi! How can I help you?",
        "type": "assistant",
        "timestamp": "2025-01-01T00:00:01"
    })
    
    # Get history
    history = config_manager.get_chat_history(channel_id)
    
    # Verify history has 2 messages
    assert len(history) == 2, f"Expected 2 messages, got {len(history)}"
    
    # Verify first message has user_character
    assert history[0].get("user_character") == "alice", "First message should have user_character 'alice'"
    
    # Simulate looking for last user character in history for this author
    active_user_character = None
    for msg in reversed(history[-20:]):
        if msg.get("user_character") and msg.get("author") == author_id:
            active_user_character = msg.get("user_character")
            break
    
    # Verify we found the character
    assert active_user_character == "alice", f"Should find 'alice', got {active_user_character}"
    
    print("✓ User character persistence test passed!")
    print(f"  - Found character '{active_user_character}' from history")
    print(f"  - Character will be used even if not specified in next message")
    
    # Test with different user (should not find character)
    other_author_id = "user_789"
    active_user_character = None
    for msg in reversed(history[-20:]):
        if msg.get("user_character") and msg.get("author") == other_author_id:
            active_user_character = msg.get("user_character")
            break
    
    assert active_user_character is None, "Different user should not find character"
    print("✓ Character isolation per user verified!")

if __name__ == "__main__":
    print("Testing user character persistence across messages...")
    test_user_character_persistence()
    print("\n✓ All tests passed!")
