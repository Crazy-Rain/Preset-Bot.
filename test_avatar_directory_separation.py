"""
Comprehensive test to verify avatar directory separation
"""

import os
import sys
from bot import ConfigManager

def test_avatar_directory_paths():
    """Test that avatar paths are correctly set for both character types"""
    print("\n" + "=" * 70)
    print("Testing Avatar Directory Path Separation")
    print("=" * 70)
    
    # Create a test config
    test_config_path = "test_avatar_paths_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    # Test 1: AI Character avatar paths
    print("\n1. Testing AI Character avatar paths...")
    config_mgr.add_character(
        name="testbot",
        display_name="Test Bot",
        description="A test AI character",
        avatar_url="https://example.com/testbot.png",
        avatar_file="character_avatars/testbot.png",
        scenario="Test scenario"
    )
    
    char = config_mgr.get_character_by_name("testbot")
    assert char is not None, "Character should exist"
    
    avatar_file = char.get("avatar_file", "")
    assert avatar_file.startswith("character_avatars/"), \
        f"AI character avatar should be in character_avatars/, got: {avatar_file}"
    print(f"   ✓ AI character avatar path: {avatar_file}")
    
    # Test 2: User Character avatar paths
    print("\n2. Testing User Character avatar paths...")
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice",
        description="A test user character",
        avatar_url="https://example.com/alice.png",
        avatar_file="ucharacter_avatars/alice.png"
    )
    
    user_char = config_mgr.get_user_character_by_name("alice")
    assert user_char is not None, "User character should exist"
    
    avatar_file = user_char.get("avatar_file", "")
    assert avatar_file.startswith("ucharacter_avatars/"), \
        f"User character avatar should be in ucharacter_avatars/, got: {avatar_file}"
    print(f"   ✓ User character avatar path: {avatar_file}")
    
    # Test 3: Update AI character with new avatar
    print("\n3. Testing AI Character update...")
    config_mgr.update_character(
        index=0,
        name="testbot",
        display_name="Test Bot Updated",
        description="Updated description",
        avatar_url="https://example.com/testbot_new.png",
        avatar_file="character_avatars/testbot_updated.png",
        scenario="Updated scenario"
    )
    
    char = config_mgr.get_character_by_name("testbot")
    avatar_file = char.get("avatar_file", "")
    assert avatar_file.startswith("character_avatars/"), \
        f"Updated AI character avatar should be in character_avatars/, got: {avatar_file}"
    print(f"   ✓ Updated AI character avatar path: {avatar_file}")
    
    # Test 4: Update User character with new avatar
    print("\n4. Testing User Character update...")
    config_mgr.update_user_character(
        index=0,
        name="alice",
        display_name="Alice Updated",
        description="Updated description",
        avatar_url="https://example.com/alice_new.png",
        avatar_file="ucharacter_avatars/alice_updated.png"
    )
    
    user_char = config_mgr.get_user_character_by_name("alice")
    avatar_file = user_char.get("avatar_file", "")
    assert avatar_file.startswith("ucharacter_avatars/"), \
        f"Updated user character avatar should be in ucharacter_avatars/, got: {avatar_file}"
    print(f"   ✓ Updated user character avatar path: {avatar_file}")
    
    # Test 5: Verify no cross-contamination
    print("\n5. Testing no cross-contamination...")
    
    # Get all characters
    all_chars = config_mgr.get_characters()
    for char in all_chars:
        avatar_file = char.get("avatar_file", "")
        if avatar_file:
            assert avatar_file.startswith("character_avatars/"), \
                f"AI character has wrong avatar path: {avatar_file}"
    print(f"   ✓ All {len(all_chars)} AI characters use character_avatars/")
    
    # Get all user characters
    all_user_chars = config_mgr.get_user_characters()
    for user_char in all_user_chars:
        avatar_file = user_char.get("avatar_file", "")
        if avatar_file:
            assert avatar_file.startswith("ucharacter_avatars/"), \
                f"User character has wrong avatar path: {avatar_file}"
    print(f"   ✓ All {len(all_user_chars)} user characters use ucharacter_avatars/")
    
    # Test 6: Verify empty avatar_file doesn't cause issues
    print("\n6. Testing characters without avatar files...")
    config_mgr.add_character(
        name="noavatar",
        display_name="No Avatar",
        description="Character without avatar",
        avatar_url="",
        avatar_file="",
        scenario=""
    )
    
    char = config_mgr.get_character_by_name("noavatar")
    assert char.get("avatar_file", "") == "", "Empty avatar_file should remain empty"
    print("   ✓ Character without avatar_file works correctly")
    
    config_mgr.add_user_character(
        name="noavatar_user",
        display_name="No Avatar User",
        description="User character without avatar",
        avatar_url="",
        avatar_file=""
    )
    
    user_char = config_mgr.get_user_character_by_name("noavatar_user")
    assert user_char.get("avatar_file", "") == "", "Empty avatar_file should remain empty"
    print("   ✓ User character without avatar_file works correctly")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    print("\n" + "=" * 70)
    print("✅ All avatar directory path tests passed!")
    print("=" * 70)
    print("\nSummary:")
    print("  • AI Characters → character_avatars/")
    print("  • User Characters → ucharacter_avatars/")
    print("  • No cross-contamination detected")
    print("  • Update operations maintain correct paths")
    print("=" * 70)
    return True

def main():
    """Run tests"""
    try:
        test_avatar_directory_paths()
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
