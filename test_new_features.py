#!/usr/bin/env python3
"""
Test new features: scenario field, edit functionality, and AI config options
"""

import os
import json
from bot import ConfigManager

def test_scenario_field():
    """Test that scenario field works correctly"""
    print("\n" + "="*60)
    print("Testing Scenario Field")
    print("="*60)
    
    # Create test config
    test_config = "test_scenario_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add a character with scenario
    config_mgr.add_character(
        name="storyteller",
        display_name="Story Teller",
        description="You are a creative storyteller.",
        scenario="You are in a fantasy tavern, ready to tell stories to adventurers.",
        avatar_url="",
        avatar_file=""
    )
    
    # Verify scenario was saved
    char = config_mgr.get_character_by_name("storyteller")
    assert char is not None, "Character not found"
    assert char.get("scenario", "") == "You are in a fantasy tavern, ready to tell stories to adventurers.", "Scenario not saved correctly"
    
    print("✓ Scenario field saved correctly")
    print(f"  Character: {char['display_name']}")
    print(f"  Scenario: {char['scenario']}")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_update_character():
    """Test update_character method"""
    print("\n" + "="*60)
    print("Testing Update Character")
    print("="*60)
    
    # Create test config
    test_config = "test_update_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add a character
    config_mgr.add_character(
        name="helper",
        display_name="Helper",
        description="Original description",
        scenario="Original scenario",
        avatar_url="",
        avatar_file=""
    )
    
    # Update the character
    config_mgr.update_character(
        index=0,
        name="helper",
        display_name="Super Helper",
        description="Updated description",
        scenario="Updated scenario",
        avatar_url="https://example.com/avatar.png",
        avatar_file=""
    )
    
    # Verify update
    char = config_mgr.get_character_by_name("helper")
    assert char is not None, "Character not found"
    assert char["display_name"] == "Super Helper", "Display name not updated"
    assert char["description"] == "Updated description", "Description not updated"
    assert char["scenario"] == "Updated scenario", "Scenario not updated"
    assert char["avatar_url"] == "https://example.com/avatar.png", "Avatar URL not updated"
    
    print("✓ Character updated successfully")
    print(f"  Display Name: {char['display_name']}")
    print(f"  Description: {char['description']}")
    print(f"  Scenario: {char['scenario']}")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_update_user_character():
    """Test update_user_character method"""
    print("\n" + "="*60)
    print("Testing Update User Character")
    print("="*60)
    
    # Create test config
    test_config = "test_update_user_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Add a user character
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice",
        description="Original description",
        avatar_url="",
        avatar_file=""
    )
    
    # Update the user character
    config_mgr.update_user_character(
        index=0,
        name="alice",
        display_name="Alice Smith",
        description="Updated description",
        avatar_url="https://example.com/alice.png",
        avatar_file=""
    )
    
    # Verify update
    char = config_mgr.get_user_character_by_name("alice")
    assert char is not None, "User character not found"
    assert char["display_name"] == "Alice Smith", "Display name not updated"
    assert char["description"] == "Updated description", "Description not updated"
    assert char["avatar_url"] == "https://example.com/alice.png", "Avatar URL not updated"
    
    print("✓ User character updated successfully")
    print(f"  Display Name: {char['display_name']}")
    print(f"  Description: {char['description']}")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def test_ai_config_options():
    """Test AI configuration options save/load"""
    print("\n" + "="*60)
    print("Testing AI Config Options")
    print("="*60)
    
    # Create test config
    test_config = "test_ai_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Set AI config options
    ai_options = {
        "max_tokens": 8192,
        "response_length": 2048,
        "temperature": 0.8,
        "top_p": 0.95,
        "reasoning_enabled": True,
        "reasoning_level": "High",
        "use_presence_penalty": True,
        "presence_penalty": 0.5,
        "use_frequency_penalty": True,
        "frequency_penalty": 0.3
    }
    config_mgr.set_ai_config_options(ai_options)
    
    # Verify options were saved
    loaded_options = config_mgr.get_ai_config_options()
    assert loaded_options["max_tokens"] == 8192, "Max tokens not saved"
    assert loaded_options["temperature"] == 0.8, "Temperature not saved"
    assert loaded_options["reasoning_enabled"] == True, "Reasoning enabled not saved"
    assert loaded_options["reasoning_level"] == "High", "Reasoning level not saved"
    
    print("✓ AI config options saved successfully")
    print(f"  Max Tokens: {loaded_options['max_tokens']}")
    print(f"  Temperature: {loaded_options['temperature']}")
    print(f"  Reasoning: {loaded_options['reasoning_enabled']} ({loaded_options['reasoning_level']})")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  New Features Test Suite")
    print("="*60)
    
    tests = [
        ("Scenario Field", test_scenario_field),
        ("Update Character", test_update_character),
        ("Update User Character", test_update_user_character),
        ("AI Config Options", test_ai_config_options),
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
