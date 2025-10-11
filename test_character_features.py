#!/usr/bin/env python3
"""
Test new character features
"""

import os
import json
from bot import ConfigManager

def test_new_character_structure():
    """Test the new character structure with all fields"""
    print("\n" + "="*60)
    print("Testing New Character Structure")
    print("="*60)
    
    # Create test config
    test_config = "test_char_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add a character with new structure
    config_mgr.add_character(
        name="tech_expert",
        display_name="Tech Expert",
        description="You are a technical expert who provides detailed solutions.",
        avatar_url="https://example.com/avatar.png",
        avatar_file=""
    )
    
    # Verify it was added
    chars = config_mgr.get_characters()
    assert len(chars) >= 1, "Character not added"
    
    # Find our character
    tech_expert = config_mgr.get_character_by_name("tech_expert")
    assert tech_expert is not None, "Character not found"
    assert tech_expert["name"] == "tech_expert", "Name mismatch"
    assert tech_expert["display_name"] == "Tech Expert", "Display name mismatch"
    assert "technical expert" in tech_expert["description"], "Description mismatch"
    assert tech_expert["avatar_url"] == "https://example.com/avatar.png", "Avatar URL mismatch"
    
    print("✓ Character created with all new fields")
    print(f"  Name: {tech_expert['name']}")
    print(f"  Display Name: {tech_expert['display_name']}")
    print(f"  Description: {tech_expert['description'][:50]}...")
    print(f"  Avatar URL: {tech_expert['avatar_url']}")
    
    # Test update
    config_mgr.update_character(
        index=len(chars)-1,
        name="tech_expert",
        display_name="Tech Expert Pro",
        description="Updated description",
        avatar_url="https://example.com/new-avatar.png",
        avatar_file=""
    )
    
    tech_expert = config_mgr.get_character_by_name("tech_expert")
    assert tech_expert["display_name"] == "Tech Expert Pro", "Update failed"
    print("✓ Character updated successfully")
    
    # Test delete
    initial_count = len(config_mgr.get_characters())
    config_mgr.delete_character(len(chars)-1)
    assert len(config_mgr.get_characters()) == initial_count - 1, "Delete failed"
    print("✓ Character deleted successfully")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_backward_compatibility():
    """Test that old format still works"""
    print("\n" + "="*60)
    print("Testing Backward Compatibility")
    print("="*60)
    
    # Create config with old format
    test_config = "test_compat_config.json"
    old_format = {
        "discord": {"token": ""},
        "openai": {"base_url": "https://api.openai.com/v1", "api_key": ""},
        "characters": [
            {
                "name": "OldBot",
                "system_prompt": "You are a helpful assistant."
            }
        ]
    }
    
    with open(test_config, 'w') as f:
        json.dump(old_format, f)
    
    # Load and verify
    config_mgr = ConfigManager(test_config)
    chars = config_mgr.get_characters()
    assert len(chars) == 1, "Old format not loaded"
    assert chars[0]["name"] == "OldBot", "Old character not found"
    
    # Should have system_prompt field
    assert "system_prompt" in chars[0], "system_prompt field missing"
    print("✓ Old format characters still work")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Backward compatibility verified")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Character Features Test Suite")
    print("="*60)
    
    tests = [
        ("New Character Structure", test_new_character_structure),
        ("Backward Compatibility", test_backward_compatibility),
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
