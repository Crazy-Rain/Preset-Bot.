#!/usr/bin/env python3
"""
Test Lorebook Functionality
"""

import os
import json
from bot import ConfigManager


def test_lorebook_management():
    """Test lorebook CRUD operations"""
    print("\n" + "="*60)
    print("Testing Lorebook Management")
    print("="*60)
    
    # Create test config
    test_config = "test_lorebook.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Test adding lorebook
    config_mgr.add_lorebook("fantasy_world", active=True)
    lorebooks = config_mgr.get_lorebooks()
    assert len(lorebooks) == 1, "Lorebook not added"
    assert lorebooks[0]["name"] == "fantasy_world", "Lorebook name incorrect"
    assert lorebooks[0]["active"] == True, "Lorebook should be active"
    print("✓ Lorebook created successfully")
    
    # Test getting lorebook by name
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert lorebook is not None, "Could not find lorebook by name"
    assert lorebook["name"] == "fantasy_world", "Retrieved wrong lorebook"
    print("✓ Lorebook retrieved by name")
    
    # Test adding another lorebook
    config_mgr.add_lorebook("sci_fi_world", active=False)
    lorebooks = config_mgr.get_lorebooks()
    assert len(lorebooks) == 2, "Second lorebook not added"
    print("✓ Multiple lorebooks supported")
    
    # Test toggling lorebook active state
    result = config_mgr.toggle_lorebook_active("fantasy_world", False)
    assert result == True, "Toggle failed"
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert lorebook["active"] == False, "Lorebook not deactivated"
    print("✓ Lorebook deactivated")
    
    result = config_mgr.toggle_lorebook_active("fantasy_world", True)
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert lorebook["active"] == True, "Lorebook not activated"
    print("✓ Lorebook activated")
    
    # Test deleting lorebook
    index = config_mgr.get_lorebook_index_by_name("sci_fi_world")
    config_mgr.delete_lorebook(index)
    lorebooks = config_mgr.get_lorebooks()
    assert len(lorebooks) == 1, "Lorebook not deleted"
    print("✓ Lorebook deleted")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def test_lorebook_entries():
    """Test lorebook entry management"""
    print("\n" + "="*60)
    print("Testing Lorebook Entries")
    print("="*60)
    
    # Create test config
    test_config = "test_lorebook_entries.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Create a lorebook
    config_mgr.add_lorebook("test_world", active=True)
    
    # Test adding constant entry
    result = config_mgr.add_lorebook_entry(
        "test_world",
        "The sky is purple in this world.",
        insertion_type="constant"
    )
    assert result == True, "Failed to add constant entry"
    lorebook = config_mgr.get_lorebook_by_name("test_world")
    assert len(lorebook["entries"]) == 1, "Entry not added"
    assert lorebook["entries"][0]["insertion_type"] == "constant", "Wrong entry type"
    print("✓ Constant entry added")
    
    # Test adding normal entry with keywords
    result = config_mgr.add_lorebook_entry(
        "test_world",
        "Dragons are friendly creatures here.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    assert result == True, "Failed to add normal entry"
    lorebook = config_mgr.get_lorebook_by_name("test_world")
    assert len(lorebook["entries"]) == 2, "Second entry not added"
    assert lorebook["entries"][1]["insertion_type"] == "normal", "Wrong entry type"
    assert "dragon" in lorebook["entries"][1]["keywords"], "Keywords not saved"
    print("✓ Normal entry with keywords added")
    
    # Test updating entry
    result = config_mgr.update_lorebook_entry(
        "test_world",
        0,
        "The sky is bright purple in this world.",
        "constant"
    )
    assert result == True, "Failed to update entry"
    lorebook = config_mgr.get_lorebook_by_name("test_world")
    assert "bright purple" in lorebook["entries"][0]["content"], "Entry not updated"
    print("✓ Entry updated")
    
    # Test deleting entry
    result = config_mgr.delete_lorebook_entry("test_world", 0)
    assert result == True, "Failed to delete entry"
    lorebook = config_mgr.get_lorebook_by_name("test_world")
    assert len(lorebook["entries"]) == 1, "Entry not deleted"
    print("✓ Entry deleted")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def test_active_lorebook_entries():
    """Test getting active lorebook entries based on message"""
    print("\n" + "="*60)
    print("Testing Active Lorebook Entry Retrieval")
    print("="*60)
    
    # Create test config
    test_config = "test_active_entries.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Create lorebooks
    config_mgr.add_lorebook("world_info", active=True)
    config_mgr.add_lorebook("character_info", active=False)
    
    # Add entries to active lorebook
    config_mgr.add_lorebook_entry(
        "world_info",
        "This is a fantasy world.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "world_info",
        "Dragons are majestic creatures.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    config_mgr.add_lorebook_entry(
        "world_info",
        "Magic is common in this realm.",
        insertion_type="normal",
        keywords=["magic", "spell"]
    )
    
    # Add entry to inactive lorebook (should not be retrieved)
    config_mgr.add_lorebook_entry(
        "character_info",
        "This should not appear.",
        insertion_type="constant"
    )
    
    # Test with message that has no keywords
    message = "Hello, how are you?"
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 1, "Should only get constant entry"
    assert "fantasy world" in entries[0], "Wrong constant entry"
    print("✓ Constant entries retrieved correctly")
    
    # Test with message containing 'dragon' keyword
    message = "Tell me about dragons in this world."
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, f"Should get constant + dragon entry, got {len(entries)}"
    assert any("fantasy world" in e for e in entries), "Missing constant entry"
    assert any("Dragons are majestic" in e for e in entries), "Missing dragon entry"
    print("✓ Keyword-triggered entry retrieved")
    
    # Test with message containing 'magic' keyword
    message = "Can you teach me a spell?"
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, "Should get constant + magic entry"
    assert any("Magic is common" in e for e in entries), "Missing magic entry"
    print("✓ Different keyword-triggered entry retrieved")
    
    # Test with message containing multiple keywords
    message = "Are dragons able to use magic?"
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 3, f"Should get constant + both entries, got {len(entries)}"
    print("✓ Multiple keyword entries retrieved")
    
    # Test that inactive lorebook entries are not retrieved
    assert not any("should not appear" in e for e in entries), "Inactive lorebook entry appeared"
    print("✓ Inactive lorebook entries excluded")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def test_config_persistence():
    """Test that lorebook configuration persists"""
    print("\n" + "="*60)
    print("Testing Lorebook Config Persistence")
    print("="*60)
    
    # Create test config
    test_config = "test_persistence.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    # Create and populate
    config_mgr1 = ConfigManager(test_config)
    config_mgr1.add_lorebook("persistent_world", active=True)
    config_mgr1.add_lorebook_entry(
        "persistent_world",
        "Test content",
        insertion_type="constant"
    )
    
    # Load in new instance
    config_mgr2 = ConfigManager(test_config)
    lorebooks = config_mgr2.get_lorebooks()
    assert len(lorebooks) == 1, "Lorebook not persisted"
    assert lorebooks[0]["name"] == "persistent_world", "Wrong lorebook loaded"
    assert len(lorebooks[0]["entries"]) == 1, "Entry not persisted"
    print("✓ Lorebook configuration persisted correctly")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Lorebook Feature - Test Suite")
    print("="*60)
    
    tests = [
        ("Lorebook Management", test_lorebook_management),
        ("Lorebook Entries", test_lorebook_entries),
        ("Active Entry Retrieval", test_active_lorebook_entries),
        ("Config Persistence", test_config_persistence),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, "FAIL"))
    
    # Print summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    for test_name, status in results:
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {status} - {test_name}")
    
    print("="*60)
    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return all(status == "PASS" for _, status in results)


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
