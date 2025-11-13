#!/usr/bin/env python3
"""
Test Suite for Interactive Lorebook Management Feature

This script tests the Discord-based lorebook management UI.
"""

import os
import sys
import asyncio


def test_lorebook_ui_imports():
    """Test that the lorebook UI classes can be imported"""
    print("\n" + "="*60)
    print("Testing Lorebook UI Imports")
    print("="*60)
    
    try:
        from bot import (
            LorebookManagementView, 
            CreateLorebookModal, 
            AddLorebookEntryModal,
            ConfirmDeleteView
        )
        print("✓ LorebookManagementView imported successfully")
        print("✓ CreateLorebookModal imported successfully")
        print("✓ AddLorebookEntryModal imported successfully")
        print("✓ ConfirmDeleteView imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import lorebook UI classes: {str(e)}")
        return False


async def test_lorebook_views_initialization_async():
    """Test that lorebook views can be initialized (async)"""
    from bot import (
        ConfigManager, 
        LorebookManagementView, 
        CreateLorebookModal,
        AddLorebookEntryModal,
        ConfirmDeleteView
    )
    
    # Create config manager
    test_config_path = "test_config_lorebook_ui.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Add a test lorebook
    config_mgr.add_lorebook("test_lorebook", active=True)
    print("✓ Test lorebook added")
    
    # Test LorebookManagementView initialization
    try:
        view = LorebookManagementView(config_mgr, timeout=180)
        assert view is not None, "LorebookManagementView is None"
        assert view.timeout == 180, "LorebookManagementView timeout not set correctly"
        print("✓ LorebookManagementView initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize LorebookManagementView: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test CreateLorebookModal initialization
    try:
        modal = CreateLorebookModal(config_mgr)
        assert modal is not None, "CreateLorebookModal is None"
        print("✓ CreateLorebookModal initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize CreateLorebookModal: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test AddLorebookEntryModal initialization
    try:
        modal = AddLorebookEntryModal(config_mgr, "test_lorebook")
        assert modal is not None, "AddLorebookEntryModal is None"
        print("✓ AddLorebookEntryModal initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize AddLorebookEntryModal: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test ConfirmDeleteView initialization
    try:
        view = ConfirmDeleteView(config_mgr, 0, "test_lorebook", 0)
        assert view is not None, "ConfirmDeleteView is None"
        print("✓ ConfirmDeleteView initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize ConfirmDeleteView: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_lorebook_views_initialization():
    """Test that lorebook views can be initialized"""
    print("\n" + "="*60)
    print("Testing Lorebook View Initialization")
    print("="*60)
    
    return asyncio.run(test_lorebook_views_initialization_async())


async def test_lorebook_management_view_buttons_async():
    """Test that LorebookManagementView has correct buttons"""
    from bot import ConfigManager, LorebookManagementView
    
    test_config_path = "test_config_buttons.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    try:
        config_mgr = ConfigManager(test_config_path)
        
        # Add test lorebooks
        config_mgr.add_lorebook("lorebook1", active=True)
        config_mgr.add_lorebook("lorebook2", active=False)
        
        view = LorebookManagementView(config_mgr)
        
        # Count components
        component_count = len(view.children)
        print(f"✓ LorebookManagementView has {component_count} interactive components")
        
        # Check for expected buttons/selects
        button_labels = [child.label for child in view.children if hasattr(child, 'label')]
        print(f"✓ Found buttons: {button_labels}")
        
        # Verify essential buttons exist
        assert "➕ Create Lorebook" in button_labels, "Create Lorebook button missing"
        print("✓ 'Create Lorebook' button found")
        
        assert "🔄 Toggle Active/Inactive" in button_labels, "Toggle button missing"
        print("✓ 'Toggle Active/Inactive' button found")
        
        assert "📝 Add Entry" in button_labels, "Add Entry button missing"
        print("✓ 'Add Entry' button found")
        
        assert "👁️ View Entries" in button_labels, "View Entries button missing"
        print("✓ 'View Entries' button found")
        
        assert "🗑️ Delete Lorebook" in button_labels, "Delete button missing"
        print("✓ 'Delete Lorebook' button found")
        
        assert "❌ Close" in button_labels, "Close button missing"
        print("✓ 'Close' button found")
        
        # Check for select menu
        has_select = any(hasattr(child, 'placeholder') for child in view.children)
        assert has_select, "Select menu not found"
        print("✓ Select menu found")
        
        # Clean up
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        print("✓ Test cleanup complete")
        
        return True
    except AssertionError as e:
        print(f"✗ Assertion failed: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    except Exception as e:
        print(f"✗ Error testing buttons: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False


def test_lorebook_management_view_buttons():
    """Test that LorebookManagementView has correct buttons"""
    print("\n" + "="*60)
    print("Testing Lorebook Management View Buttons")
    print("="*60)
    
    return asyncio.run(test_lorebook_management_view_buttons_async())


async def test_create_lorebook_modal_fields_async():
    """Test that CreateLorebookModal has correct fields"""
    from bot import ConfigManager, CreateLorebookModal
    
    test_config_path = "test_config_modal.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    try:
        config_mgr = ConfigManager(test_config_path)
        modal = CreateLorebookModal(config_mgr)
        
        # Count fields
        field_count = len(modal.children)
        print(f"✓ CreateLorebookModal has {field_count} input field(s)")
        
        # Check field labels
        field_labels = [child.label for child in modal.children if hasattr(child, 'label')]
        print(f"✓ Field labels: {field_labels}")
        
        assert "Lorebook Name" in field_labels, "Lorebook Name field missing"
        print("✓ 'Lorebook Name' field found")
        
        # Clean up
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        print("✓ Test cleanup complete")
        
        return True
    except AssertionError as e:
        print(f"✗ Assertion failed: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    except Exception as e:
        print(f"✗ Error testing modal fields: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False


def test_create_lorebook_modal_fields():
    """Test that CreateLorebookModal has correct fields"""
    print("\n" + "="*60)
    print("Testing CreateLorebookModal Fields")
    print("="*60)
    
    return asyncio.run(test_create_lorebook_modal_fields_async())


async def test_add_entry_modal_fields_async():
    """Test that AddLorebookEntryModal has correct fields"""
    from bot import ConfigManager, AddLorebookEntryModal
    
    test_config_path = "test_config_entry_modal.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    try:
        config_mgr = ConfigManager(test_config_path)
        config_mgr.add_lorebook("test_lorebook", active=True)
        
        modal = AddLorebookEntryModal(config_mgr, "test_lorebook")
        
        # Count fields
        field_count = len(modal.children)
        print(f"✓ AddLorebookEntryModal has {field_count} input field(s)")
        
        # Check field labels
        field_labels = [child.label for child in modal.children if hasattr(child, 'label')]
        print(f"✓ Field labels: {field_labels}")
        
        assert "Entry Content" in field_labels, "Entry Content field missing"
        print("✓ 'Entry Content' field found")
        
        assert "Entry Type" in field_labels, "Entry Type field missing"
        print("✓ 'Entry Type' field found")
        
        assert "Keywords (for normal entries)" in field_labels, "Keywords field missing"
        print("✓ 'Keywords' field found")
        
        # Clean up
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        print("✓ Test cleanup complete")
        
        return True
    except AssertionError as e:
        print(f"✗ Assertion failed: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    except Exception as e:
        print(f"✗ Error testing modal fields: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False


def test_add_entry_modal_fields():
    """Test that AddLorebookEntryModal has correct fields"""
    print("\n" + "="*60)
    print("Testing AddLorebookEntryModal Fields")
    print("="*60)
    
    return asyncio.run(test_add_entry_modal_fields_async())


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Interactive Lorebook Management - Test Suite")
    print("="*60)
    
    tests = [
        ("Lorebook UI Imports", test_lorebook_ui_imports),
        ("Lorebook View Initialization", test_lorebook_views_initialization),
        ("Lorebook Management View Buttons", test_lorebook_management_view_buttons),
        ("CreateLorebookModal Fields", test_create_lorebook_modal_fields),
        ("AddLorebookEntryModal Fields", test_add_entry_modal_fields),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"\n✅ PASS - {test_name}\n")
                passed += 1
            else:
                print(f"\n❌ FAIL - {test_name}\n")
                failed += 1
        except Exception as e:
            print(f"\n❌ FAIL - {test_name}")
            print(f"Exception: {str(e)}\n")
            failed += 1
    
    print("="*60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
