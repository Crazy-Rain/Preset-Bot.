"""
Test the !set command functionality
"""

import os
import sys
from bot import ConfigManager

def test_set_command_logic():
    """Test the logic of the !set command"""
    print("\n" + "=" * 60)
    print("Testing !set Command Logic")
    print("=" * 60)
    
    # Create a test config
    test_config_path = "test_set_command_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    # Add user characters
    print("\n1. Creating user characters...")
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice the Brave",
        description="A brave knight"
    )
    
    config_mgr.add_user_character(
        name="bob",
        display_name="Bob the Wizard",
        description="A wise wizard"
    )
    print("   ✓ Created alice and bob")
    
    # Simulate !set command
    print("\n2. Simulating !set alice command...")
    channel_id = "test_channel_123"
    user_id = "user_111"
    
    # This is what the !set command does
    message_data = {
        "author": user_id,
        "author_name": "TestUser",
        "user_character": "alice",
        "content": "[Set active character to Alice the Brave]",
        "type": "system",
        "timestamp": "2024-01-01T00:00:00"
    }
    config_mgr.add_chat_message(channel_id, message_data)
    print("   ✓ Set command executed")
    
    # Now verify !viewu would find it
    print("\n3. Verifying !viewu would find the character...")
    chat_history = config_mgr.get_chat_history(channel_id)
    history_limit = config_mgr.get_chat_history_limit()
    
    active_user_character = None
    for msg in reversed(chat_history[-history_limit:]):
        if msg.get("user_character") and msg.get("author") == user_id:
            active_user_character = msg.get("user_character")
            break
    
    assert active_user_character == "alice", f"Should find alice, got {active_user_character}"
    print(f"   ✓ !viewu would correctly show: {active_user_character}")
    
    # Test changing character with !set
    print("\n4. Simulating !set bob command...")
    message_data = {
        "author": user_id,
        "author_name": "TestUser",
        "user_character": "bob",
        "content": "[Set active character to Bob the Wizard]",
        "type": "system",
        "timestamp": "2024-01-01T00:01:00"
    }
    config_mgr.add_chat_message(channel_id, message_data)
    print("   ✓ Set command executed")
    
    # Verify it changed
    print("\n5. Verifying character changed...")
    chat_history = config_mgr.get_chat_history(channel_id)
    
    active_user_character = None
    for msg in reversed(chat_history[-history_limit:]):
        if msg.get("user_character") and msg.get("author") == user_id:
            active_user_character = msg.get("user_character")
            break
    
    assert active_user_character == "bob", f"Should find bob now, got {active_user_character}"
    print(f"   ✓ !viewu would correctly show updated character: {active_user_character}")
    
    # Test that !chat still works after !set
    print("\n6. Simulating !chat after !set...")
    message_data = {
        "author": user_id,
        "author_name": "TestUser",
        "user_character": "bob",  # !chat would use the same character
        "content": "Hello from Bob!",
        "type": "user",
        "timestamp": "2024-01-01T00:02:00"
    }
    config_mgr.add_chat_message(channel_id, message_data)
    print("   ✓ !chat message added")
    
    # Verify still shows bob
    chat_history = config_mgr.get_chat_history(channel_id)
    active_user_character = None
    for msg in reversed(chat_history[-history_limit:]):
        if msg.get("user_character") and msg.get("author") == user_id:
            active_user_character = msg.get("user_character")
            break
    
    assert active_user_character == "bob", f"Should still be bob, got {active_user_character}"
    print(f"   ✓ Character persists correctly: {active_user_character}")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    print("\n" + "=" * 60)
    print("✅ All !set command tests passed!")
    print("=" * 60)
    return True

def main():
    """Run tests"""
    try:
        test_set_command_logic()
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print(traceback.format_exc())
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
