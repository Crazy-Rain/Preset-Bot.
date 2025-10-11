#!/usr/bin/env python3
"""
Test new features: user character info in chat, channel character tracking
"""

import os
import json
from bot import ConfigManager

def test_user_character_in_chat():
    """Test that user character info is properly retrieved"""
    print("\n" + "="*60)
    print("Testing User Character Info in Chat")
    print("="*60)
    
    # Create test config
    test_config = "test_user_char_chat.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add a user character
    config_mgr.add_user_character(
        name="sundial",
        display_name="Sundial",
        description="A wise and ancient pony who guards the flow of time.",
        avatar_url="",
        avatar_file=""
    )
    
    # Verify user character was saved
    user_char = config_mgr.get_user_character_by_name("sundial")
    assert user_char is not None, "User character not found"
    assert user_char["display_name"] == "Sundial", "Display name mismatch"
    assert "ancient pony" in user_char["description"], "Description mismatch"
    
    print("✓ User character created and retrieved successfully")
    print(f"  Name: {user_char['name']}")
    print(f"  Display Name: {user_char['display_name']}")
    print(f"  Description: {user_char['description']}")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_channel_character_tracking():
    """Test channel-specific character tracking"""
    print("\n" + "="*60)
    print("Testing Channel Character Tracking")
    print("="*60)
    
    # Create test config
    test_config = "test_channel_chars.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add some characters
    config_mgr.add_character(
        name="dashie",
        display_name="Rainbow Dash",
        description="You are Rainbow Dash, the fastest pony in Equestria!",
        scenario="",
        avatar_url="",
        avatar_file=""
    )
    
    config_mgr.add_character(
        name="twilight",
        display_name="Twilight Sparkle",
        description="You are Twilight Sparkle, Princess of Friendship.",
        scenario="",
        avatar_url="",
        avatar_file=""
    )
    
    # Test setting channel character
    config_mgr.set_channel_character("12345", "dashie")
    channel_char = config_mgr.get_channel_character("12345")
    assert channel_char == "dashie", "Channel character not set correctly"
    print("✓ Channel character set successfully")
    print(f"  Channel 12345 -> Character: {channel_char}")
    
    # Test different channel
    config_mgr.set_channel_character("67890", "twilight")
    channel_char2 = config_mgr.get_channel_character("67890")
    assert channel_char2 == "twilight", "Second channel character not set correctly"
    print("✓ Different channel character set successfully")
    print(f"  Channel 67890 -> Character: {channel_char2}")
    
    # Verify first channel is still correct
    channel_char = config_mgr.get_channel_character("12345")
    assert channel_char == "dashie", "First channel character changed unexpectedly"
    print("✓ First channel character unchanged")
    
    # Test clearing channel character
    config_mgr.clear_channel_character("12345")
    channel_char = config_mgr.get_channel_character("12345")
    assert channel_char is None, "Channel character not cleared"
    print("✓ Channel character cleared successfully")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_channel_characters_in_config():
    """Test that channel_characters is in default config"""
    print("\n" + "="*60)
    print("Testing Channel Characters in Config")
    print("="*60)
    
    # Create test config
    test_config = "test_config_structure.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Verify channel_characters key exists
    assert "channel_characters" in config_mgr.config, "channel_characters not in config"
    assert isinstance(config_mgr.config["channel_characters"], dict), "channel_characters should be a dict"
    print("✓ channel_characters exists in config")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  User Character & Channel Tracking Test Suite")
    print("="*60)
    
    tests = [
        ("User Character Info", test_user_character_in_chat),
        ("Channel Character Tracking", test_channel_character_tracking),
        ("Channel Characters in Config", test_channel_characters_in_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
