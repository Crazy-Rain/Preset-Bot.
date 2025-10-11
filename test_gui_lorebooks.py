#!/usr/bin/env python3
"""
Test script to validate Lorebook GUI functionality
"""

import os
import json
from bot import ConfigManager

def test_lorebook_gui_operations():
    """Test that all lorebook operations work correctly"""
    
    # Use a temporary config file
    config_path = "test_gui_lorebook_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    print("Testing Lorebook GUI Operations...")
    print("=" * 60)
    
    # Test 1: Create lorebooks
    print("\n1. Creating lorebooks...")
    config_mgr.add_lorebook("fantasy_world", active=True)
    config_mgr.add_lorebook("sci_fi_universe", active=False)
    lorebooks = config_mgr.get_lorebooks()
    assert len(lorebooks) == 2
    assert lorebooks[0]['name'] == "fantasy_world"
    assert lorebooks[0]['active'] == True
    assert lorebooks[1]['name'] == "sci_fi_universe"
    assert lorebooks[1]['active'] == False
    print("   ✓ Lorebooks created successfully")
    
    # Test 2: Add constant entry
    print("\n2. Adding constant entry...")
    success = config_mgr.add_lorebook_entry(
        "fantasy_world",
        "This is a high-fantasy medieval world.",
        insertion_type="constant",
        keywords=[]
    )
    assert success == True
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert len(lorebook['entries']) == 1
    assert lorebook['entries'][0]['insertion_type'] == "constant"
    print("   ✓ Constant entry added successfully")
    
    # Test 3: Add normal (keyword-triggered) entries
    print("\n3. Adding normal (keyword-triggered) entries...")
    success = config_mgr.add_lorebook_entry(
        "fantasy_world",
        "Dragons are wise, ancient beings.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    assert success == True
    
    success = config_mgr.add_lorebook_entry(
        "fantasy_world",
        "Elves live in forest cities.",
        insertion_type="normal",
        keywords=["elf", "elves"]
    )
    assert success == True
    
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert len(lorebook['entries']) == 3
    assert lorebook['entries'][1]['insertion_type'] == "normal"
    assert lorebook['entries'][1]['keywords'] == ["dragon", "dragons"]
    print("   ✓ Normal entries added successfully")
    
    # Test 4: Update entry
    print("\n4. Updating entry...")
    success = config_mgr.update_lorebook_entry(
        "fantasy_world",
        1,  # Update dragon entry
        "Dragons are extremely rare and powerful creatures.",
        insertion_type="normal",
        keywords=["dragon", "dragons", "wyrm"]
    )
    assert success == True
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert "extremely rare" in lorebook['entries'][1]['content']
    assert "wyrm" in lorebook['entries'][1]['keywords']
    print("   ✓ Entry updated successfully")
    
    # Test 5: Toggle lorebook active state
    print("\n5. Toggling lorebook active state...")
    success = config_mgr.toggle_lorebook_active("fantasy_world", False)
    assert success == True
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert lorebook['active'] == False
    
    success = config_mgr.toggle_lorebook_active("fantasy_world", True)
    assert success == True
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert lorebook['active'] == True
    print("   ✓ Lorebook active state toggled successfully")
    
    # Test 6: Get active lorebook entries
    print("\n6. Testing active lorebook entry retrieval...")
    entries = config_mgr.get_active_lorebook_entries("Tell me about dragons")
    # Should get constant entry + dragon entry (2 total)
    assert len(entries) == 2
    assert any("high-fantasy medieval" in e for e in entries)
    assert any("extremely rare" in e for e in entries)
    print("   ✓ Active entries retrieved correctly (2 entries for dragon keyword)")
    
    # Test 7: Delete entry
    print("\n7. Deleting entry...")
    success = config_mgr.delete_lorebook_entry("fantasy_world", 2)  # Delete elf entry
    assert success == True
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    assert len(lorebook['entries']) == 2
    print("   ✓ Entry deleted successfully")
    
    # Test 8: Update lorebook name and active state
    print("\n8. Updating lorebook...")
    index = config_mgr.get_lorebook_index_by_name("fantasy_world")
    config_mgr.update_lorebook(index, "fantasy_realm", False)
    lorebook = config_mgr.get_lorebook_by_name("fantasy_realm")
    assert lorebook is not None
    assert lorebook['name'] == "fantasy_realm"
    assert lorebook['active'] == False
    print("   ✓ Lorebook updated successfully")
    
    # Test 9: Delete lorebook
    print("\n9. Deleting lorebook...")
    index = config_mgr.get_lorebook_index_by_name("sci_fi_universe")
    config_mgr.delete_lorebook(index)
    lorebooks = config_mgr.get_lorebooks()
    assert len(lorebooks) == 1
    assert config_mgr.get_lorebook_by_name("sci_fi_universe") is None
    print("   ✓ Lorebook deleted successfully")
    
    # Cleanup
    os.remove(config_path)
    
    print("\n" + "=" * 60)
    print("✓ All lorebook GUI operations tested successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_lorebook_gui_operations()
