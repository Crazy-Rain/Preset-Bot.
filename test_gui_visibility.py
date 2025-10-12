"""
Test script to verify GUI visibility enhancements work correctly
"""
import os
import sys
from bot import ConfigManager

def test_gui_import():
    """Test that the GUI module imports without errors"""
    try:
        import gui
        print("✓ GUI module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error importing GUI: {e}")
        return False

def test_config_manager():
    """Test that ConfigManager works with lorebook visibility"""
    config_path = "test_gui_visibility_config.json"
    
    if os.path.exists(config_path):
        os.remove(config_path)
    
    try:
        config_mgr = ConfigManager(config_path)
        
        # Create test lorebooks
        config_mgr.add_lorebook("active_book", active=True)
        config_mgr.add_lorebook("inactive_book", active=False)
        
        # Add entries
        config_mgr.add_lorebook_entry("active_book", "Active content", "constant")
        config_mgr.add_lorebook_entry("inactive_book", "Inactive content", "constant")
        
        print("✓ Created test lorebooks")
        
        # Test visibility by checking if we can retrieve lorebooks
        lorebooks = config_mgr.get_lorebooks()
        assert len(lorebooks) == 2
        print(f"✓ Found {len(lorebooks)} lorebooks")
        
        # Display lorebook status
        for lb in lorebooks:
            name = lb.get("name")
            active = lb.get("active", False)
            status = "ACTIVE ✓" if active else "INACTIVE ✗"
            print(f"  - {name}: {status}")
        
        # Test entry retrieval with logging
        print("\n✓ Testing entry retrieval (check console for visibility logs):")
        message = "test message"
        entries = config_mgr.get_active_lorebook_entries(message)
        print(f"✓ Retrieved {len(entries)} entries (should be 1 - only from active lorebook)")
        
        assert len(entries) == 1, f"Expected 1 entry from active lorebook, got {len(entries)}"
        
        # Cleanup
        os.remove(config_path)
        print("\n✓ Test cleanup complete")
        
        return True
    except Exception as e:
        print(f"✗ Error in config manager test: {e}")
        import traceback
        traceback.print_exc()
        if os.path.exists(config_path):
            os.remove(config_path)
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  GUI Visibility Enhancement - Test")
    print("=" * 60)
    print()
    
    tests_passed = 0
    total_tests = 2
    
    print("Test 1: GUI Module Import")
    if test_gui_import():
        tests_passed += 1
    print()
    
    print("Test 2: ConfigManager with Visibility Logging")
    if test_config_manager():
        tests_passed += 1
    print()
    
    print("=" * 60)
    print(f"Results: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
