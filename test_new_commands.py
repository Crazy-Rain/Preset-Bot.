"""
Test the new viewu, viewc, and cimage commands
"""

import json
import os
import sys

def test_config_manager():
    """Test ConfigManager with user characters"""
    from bot import ConfigManager
    
    # Create a test config
    test_config_path = "test_new_commands_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    # Add some test characters
    config_mgr.add_character(
        name="testbot",
        display_name="Test Bot",
        description="A helpful AI assistant for testing",
        avatar_url="https://example.com/testbot.png",
        avatar_file="",
        scenario="You are in a test scenario"
    )
    
    # Add some test user characters
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice",
        description="A brave adventurer",
        avatar_url="https://example.com/alice.png"
    )
    
    config_mgr.add_user_character(
        name="bob",
        display_name="Bob",
        description="A wise wizard",
        avatar_url="https://example.com/bob.png"
    )
    
    # Test getting user characters
    alice = config_mgr.get_user_character_by_name("alice")
    assert alice is not None, "Alice character should exist"
    assert alice["display_name"] == "Alice", "Alice display name should match"
    
    bob = config_mgr.get_user_character_by_name("bob")
    assert bob is not None, "Bob character should exist"
    
    # Test getting regular characters
    testbot = config_mgr.get_character_by_name("testbot")
    assert testbot is not None, "Test Bot character should exist"
    assert testbot.get("scenario") == "You are in a test scenario", f"Scenario should match, got: {testbot.get('scenario')}"
    
    # Test channel character assignment
    config_mgr.set_channel_character("12345", "testbot")
    channel_char = config_mgr.get_channel_character("12345")
    assert channel_char == "testbot", "Channel character should be testbot"
    
    # Test chat history with user characters
    config_mgr.add_chat_message("12345", {
        "author": "user123",
        "author_name": "TestUser",
        "user_character": "alice",
        "content": "Hello!",
        "type": "user",
        "timestamp": "2024-01-01T00:00:00"
    })
    
    history = config_mgr.get_chat_history("12345")
    assert len(history) == 1, "Should have one message in history"
    assert history[0]["user_character"] == "alice", "Message should be from alice"
    
    # Test update_user_character
    config_mgr.update_user_character(
        index=0,
        name="alice",
        display_name="Alice Updated",
        description="A brave adventurer updated",
        avatar_url="https://example.com/alice_new.png",
        avatar_file="ucharacter_avatars/alice.png"
    )
    
    alice_updated = config_mgr.get_user_character_by_name("alice")
    assert alice_updated["display_name"] == "Alice Updated", "Alice should be updated"
    assert alice_updated["avatar_file"] == "ucharacter_avatars/alice.png", "Avatar file should be set"
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    return True

def test_command_logic():
    """Test the logic of finding user characters in chat history"""
    from bot import ConfigManager
    
    # Create a test config
    test_config_path = "test_command_logic_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    # Add user characters
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice",
        description="A brave adventurer"
    )
    
    config_mgr.add_user_character(
        name="bob",
        display_name="Bob",
        description="A wise wizard"
    )
    
    # Simulate chat history
    channel_id = "test_channel_123"
    user_id_1 = "user_111"
    user_id_2 = "user_222"
    
    # User 1 uses alice
    config_mgr.add_chat_message(channel_id, {
        "author": user_id_1,
        "author_name": "User1",
        "user_character": "alice",
        "content": "Hello as Alice!",
        "type": "user",
        "timestamp": "2024-01-01T00:00:00"
    })
    
    # User 2 uses bob
    config_mgr.add_chat_message(channel_id, {
        "author": user_id_2,
        "author_name": "User2",
        "user_character": "bob",
        "content": "Hello as Bob!",
        "type": "user",
        "timestamp": "2024-01-01T00:01:00"
    })
    
    # User 1 sends another message (should inherit alice)
    config_mgr.add_chat_message(channel_id, {
        "author": user_id_1,
        "author_name": "User1",
        "user_character": "alice",
        "content": "Another message!",
        "type": "user",
        "timestamp": "2024-01-01T00:02:00"
    })
    
    # Now test finding the active character for each user
    history = config_mgr.get_chat_history(channel_id)
    history_limit = config_mgr.get_chat_history_limit()
    
    # Find user1's character
    active_char_user1 = None
    for msg in reversed(history[-history_limit:]):
        if msg.get("user_character") and msg.get("author") == user_id_1:
            active_char_user1 = msg.get("user_character")
            break
    
    assert active_char_user1 == "alice", f"User1's active character should be alice, got {active_char_user1}"
    
    # Find user2's character
    active_char_user2 = None
    for msg in reversed(history[-history_limit:]):
        if msg.get("user_character") and msg.get("author") == user_id_2:
            active_char_user2 = msg.get("user_character")
            break
    
    assert active_char_user2 == "bob", f"User2's active character should be bob, got {active_char_user2}"
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("  Test Suite for New Commands (viewu, viewc, cimage)")
    print("=" * 60)
    print()
    
    tests = [
        ("ConfigManager with User Characters", test_config_manager),
        ("Command Logic for Finding User Characters", test_command_logic),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...", end=" ")
        try:
            result = test_func()
            if result:
                print("✓ PASS")
                passed += 1
            else:
                print("✗ FAIL")
                failed += 1
        except Exception as e:
            print(f"✗ FAIL - {str(e)}")
            import traceback
            print(traceback.format_exc())
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
