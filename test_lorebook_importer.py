#!/usr/bin/env python3
"""
Test the lorebook importer functionality
"""

import os
import json
from bot import ConfigManager

def test_lorebook_importer():
    """Test lorebook import functionality"""
    print("\n" + "="*60)
    print("Testing Lorebook Importer")
    print("="*60)
    
    # Create test config
    test_config = "test_import_config.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Test 1: Verify sample lorebook exists
    print("\n1. Checking sample lorebook file...")
    sample_file = "sample_lorebook.json"
    assert os.path.exists(sample_file), "Sample lorebook file not found"
    print(f"   ✓ Sample file found: {sample_file}")
    
    # Test 2: Load and validate sample lorebook structure
    print("\n2. Loading and validating lorebook structure...")
    with open(sample_file, 'r') as f:
        lorebook_data = json.load(f)
    
    assert "name" in lorebook_data, "Missing 'name' field"
    assert "entries" in lorebook_data, "Missing 'entries' field"
    assert isinstance(lorebook_data["entries"], list), "'entries' must be a list"
    print(f"   ✓ Valid lorebook structure")
    print(f"   - Name: {lorebook_data['name']}")
    print(f"   - Entries: {len(lorebook_data['entries'])}")
    
    # Test 3: Validate entry structures
    print("\n3. Validating entry structures...")
    constant_count = 0
    normal_count = 0
    
    for i, entry in enumerate(lorebook_data["entries"]):
        assert "content" in entry, f"Entry {i}: Missing 'content' field"
        assert "insertion_type" in entry, f"Entry {i}: Missing 'insertion_type' field"
        assert entry["insertion_type"] in ["constant", "normal"], f"Entry {i}: Invalid insertion_type"
        
        if entry["insertion_type"] == "constant":
            constant_count += 1
        else:
            normal_count += 1
            assert "keywords" in entry, f"Entry {i}: Normal entries must have 'keywords' field"
            assert isinstance(entry["keywords"], list), f"Entry {i}: 'keywords' must be a list"
            assert len(entry["keywords"]) > 0, f"Entry {i}: Normal entries must have at least one keyword"
    
    print(f"   ✓ All entries valid")
    print(f"   - Constant entries: {constant_count}")
    print(f"   - Normal entries: {normal_count}")
    
    # Test 4: Simulate import to new lorebook
    print("\n4. Simulating import to new lorebook...")
    target_name = "test_imported_lorebook"
    config_mgr.add_lorebook(target_name, active=True)
    
    # Import all entries
    imported_count = 0
    for entry in lorebook_data["entries"]:
        content = entry.get("content", "")
        insertion_type = entry.get("insertion_type", "normal")
        keywords = entry.get("keywords", [])
        
        if config_mgr.add_lorebook_entry(target_name, content, insertion_type, keywords):
            imported_count += 1
    
    print(f"   ✓ Imported {imported_count} entries")
    
    # Test 5: Verify imported entries
    print("\n5. Verifying imported entries...")
    imported_lb = config_mgr.get_lorebook_by_name(target_name)
    assert imported_lb is not None, "Imported lorebook not found"
    assert len(imported_lb["entries"]) == imported_count, "Entry count mismatch"
    print(f"   ✓ All entries imported successfully")
    
    # Test 6: Test filtering by type
    print("\n6. Testing entry filtering...")
    constant_entries = [e for e in imported_lb["entries"] if e["insertion_type"] == "constant"]
    normal_entries = [e for e in imported_lb["entries"] if e["insertion_type"] == "normal"]
    
    print(f"   ✓ Filtering works correctly")
    print(f"   - Constant entries: {len(constant_entries)}")
    print(f"   - Normal entries: {len(normal_entries)}")
    
    # Test 7: Test import to existing lorebook
    print("\n7. Testing import to existing lorebook...")
    existing_name = "existing_lorebook"
    config_mgr.add_lorebook(existing_name, active=True)
    
    # Import just the first 2 entries
    for entry in lorebook_data["entries"][:2]:
        content = entry.get("content", "")
        insertion_type = entry.get("insertion_type", "normal")
        keywords = entry.get("keywords", [])
        config_mgr.add_lorebook_entry(existing_name, content, insertion_type, keywords)
    
    existing_lb = config_mgr.get_lorebook_by_name(existing_name)
    assert len(existing_lb["entries"]) == 2, "Should have 2 entries"
    print(f"   ✓ Import to existing lorebook works")
    
    # Cleanup
    os.remove(test_config)
    print("\n" + "="*60)
    print("✓ All tests passed!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = test_lorebook_importer()
        sys.exit(0 if success else 1)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
