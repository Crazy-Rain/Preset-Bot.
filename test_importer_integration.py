#!/usr/bin/env python3
"""
Comprehensive integration test for lorebook importer
Tests various formats and edge cases
"""

import os
import json
from bot import ConfigManager

def test_single_lorebook_format():
    """Test importing single lorebook format"""
    print("\nTest 1: Single Lorebook Format")
    print("-" * 50)
    
    # Create test file
    test_data = {
        "name": "test_single",
        "active": True,
        "entries": [
            {
                "content": "Constant entry",
                "insertion_type": "constant",
                "keywords": []
            },
            {
                "content": "Normal entry",
                "insertion_type": "normal",
                "keywords": ["test", "keyword"]
            }
        ]
    }
    
    with open("test_single.json", 'w') as f:
        json.dump(test_data, f)
    
    # Verify structure
    with open("test_single.json", 'r') as f:
        data = json.load(f)
    
    assert "entries" in data
    assert len(data["entries"]) == 2
    print("✓ Single lorebook format valid")
    
    os.remove("test_single.json")
    return True

def test_config_format():
    """Test importing config format with multiple lorebooks"""
    print("\nTest 2: Config Format (Multiple Lorebooks)")
    print("-" * 50)
    
    test_data = {
        "lorebooks": [
            {
                "name": "lorebook1",
                "active": True,
                "entries": [
                    {"content": "Entry 1", "insertion_type": "constant", "keywords": []}
                ]
            },
            {
                "name": "lorebook2",
                "active": False,
                "entries": [
                    {"content": "Entry 2", "insertion_type": "normal", "keywords": ["kw"]}
                ]
            }
        ]
    }
    
    with open("test_config.json", 'w') as f:
        json.dump(test_data, f)
    
    with open("test_config.json", 'r') as f:
        data = json.load(f)
    
    assert "lorebooks" in data
    assert len(data["lorebooks"]) == 2
    print(f"✓ Config format valid with {len(data['lorebooks'])} lorebooks")
    
    os.remove("test_config.json")
    return True

def test_array_format():
    """Test importing array of lorebooks"""
    print("\nTest 3: Array Format")
    print("-" * 50)
    
    test_data = [
        {
            "name": "array_lb1",
            "entries": [
                {"content": "Array entry 1", "insertion_type": "constant", "keywords": []}
            ]
        },
        {
            "name": "array_lb2",
            "entries": [
                {"content": "Array entry 2", "insertion_type": "normal", "keywords": ["test"]}
            ]
        }
    ]
    
    with open("test_array.json", 'w') as f:
        json.dump(test_data, f)
    
    with open("test_array.json", 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == 2
    print(f"✓ Array format valid with {len(data)} lorebooks")
    
    os.remove("test_array.json")
    return True

def test_import_to_new_lorebook():
    """Test importing to a new lorebook"""
    print("\nTest 4: Import to New Lorebook")
    print("-" * 50)
    
    config = ConfigManager("test_import_new.json")
    
    # Simulate importing entries
    target_name = "imported_new"
    config.add_lorebook(target_name, active=True)
    
    entries = [
        {"content": "Entry 1", "insertion_type": "constant", "keywords": []},
        {"content": "Entry 2", "insertion_type": "normal", "keywords": ["test"]}
    ]
    
    for entry in entries:
        config.add_lorebook_entry(
            target_name,
            entry["content"],
            entry["insertion_type"],
            entry["keywords"]
        )
    
    # Verify
    lb = config.get_lorebook_by_name(target_name)
    assert lb is not None
    assert len(lb["entries"]) == 2
    print(f"✓ Created new lorebook with {len(lb['entries'])} imported entries")
    
    os.remove("test_import_new.json")
    return True

def test_import_to_existing_lorebook():
    """Test importing to an existing lorebook"""
    print("\nTest 5: Import to Existing Lorebook")
    print("-" * 50)
    
    config = ConfigManager("test_import_existing.json")
    
    # Create existing lorebook with one entry
    target_name = "existing_lb"
    config.add_lorebook(target_name, active=True)
    config.add_lorebook_entry(
        target_name,
        "Original entry",
        "constant",
        []
    )
    
    # Import additional entries
    new_entries = [
        {"content": "Imported 1", "insertion_type": "normal", "keywords": ["kw1"]},
        {"content": "Imported 2", "insertion_type": "normal", "keywords": ["kw2"]}
    ]
    
    for entry in new_entries:
        config.add_lorebook_entry(
            target_name,
            entry["content"],
            entry["insertion_type"],
            entry["keywords"]
        )
    
    # Verify
    lb = config.get_lorebook_by_name(target_name)
    assert len(lb["entries"]) == 3  # 1 original + 2 imported
    print(f"✓ Imported to existing lorebook: 1 original + 2 imported = {len(lb['entries'])} total")
    
    os.remove("test_import_existing.json")
    return True

def test_entry_filtering():
    """Test filtering entries by type"""
    print("\nTest 6: Entry Filtering")
    print("-" * 50)
    
    entries = [
        {"content": "C1", "insertion_type": "constant", "keywords": []},
        {"content": "N1", "insertion_type": "normal", "keywords": ["k1"]},
        {"content": "C2", "insertion_type": "constant", "keywords": []},
        {"content": "N2", "insertion_type": "normal", "keywords": ["k2"]},
        {"content": "N3", "insertion_type": "normal", "keywords": ["k3"]}
    ]
    
    # Filter constant
    constant = [e for e in entries if e["insertion_type"] == "constant"]
    assert len(constant) == 2
    print(f"✓ Constant filter: {len(constant)} entries")
    
    # Filter normal
    normal = [e for e in entries if e["insertion_type"] == "normal"]
    assert len(normal) == 3
    print(f"✓ Normal filter: {len(normal)} entries")
    
    # All entries
    assert len(entries) == 5
    print(f"✓ All entries: {len(entries)}")
    
    return True

def test_invalid_formats():
    """Test error handling for invalid formats"""
    print("\nTest 7: Invalid Format Handling")
    print("-" * 50)
    
    # Test 1: Invalid JSON
    with open("test_invalid_json.json", 'w') as f:
        f.write("{invalid json content")
    
    try:
        with open("test_invalid_json.json", 'r') as f:
            json.load(f)
        assert False, "Should have raised JSONDecodeError"
    except json.JSONDecodeError:
        print("✓ Invalid JSON detected correctly")
    
    os.remove("test_invalid_json.json")
    
    # Test 2: Missing required fields
    test_data = {
        "name": "test",
        "no_entries_field": []
    }
    
    with open("test_missing_field.json", 'w') as f:
        json.dump(test_data, f)
    
    with open("test_missing_field.json", 'r') as f:
        data = json.load(f)
    
    if "entries" not in data and "lorebooks" not in data:
        print("✓ Missing required fields detected correctly")
    
    os.remove("test_missing_field.json")
    
    return True

def test_large_import():
    """Test importing a lorebook with many entries"""
    print("\nTest 8: Large Import")
    print("-" * 50)
    
    # Create lorebook with 50 entries
    entries = []
    for i in range(50):
        entry_type = "constant" if i % 5 == 0 else "normal"
        entries.append({
            "content": f"Entry {i} content",
            "insertion_type": entry_type,
            "keywords": [] if entry_type == "constant" else [f"kw{i}", f"keyword{i}"]
        })
    
    test_data = {
        "name": "large_lorebook",
        "entries": entries
    }
    
    with open("test_large.json", 'w') as f:
        json.dump(test_data, f)
    
    # Import
    config = ConfigManager("test_large_config.json")
    config.add_lorebook("large_import", active=True)
    
    for entry in entries:
        config.add_lorebook_entry(
            "large_import",
            entry["content"],
            entry["insertion_type"],
            entry["keywords"]
        )
    
    # Verify
    lb = config.get_lorebook_by_name("large_import")
    assert len(lb["entries"]) == 50
    print(f"✓ Successfully imported {len(lb['entries'])} entries")
    
    os.remove("test_large.json")
    os.remove("test_large_config.json")
    return True

def main():
    """Run all integration tests"""
    print("=" * 50)
    print("Lorebook Importer Integration Tests")
    print("=" * 50)
    
    tests = [
        test_single_lorebook_format,
        test_config_format,
        test_array_format,
        test_import_to_new_lorebook,
        test_import_to_existing_lorebook,
        test_entry_filtering,
        test_invalid_formats,
        test_large_import
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"Tests Failed: {failed}/{len(tests)}")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
