#!/usr/bin/env python3
"""
Test Suite for Interactive Character Management Feature

This script tests the Discord-based character management UI.
"""

import os
import sys
import asyncio


def test_character_ui_imports():
    """Test that the character UI classes can be imported"""
    print("\n" + "="*60)
    print("Testing Character UI Imports")
    print("="*60)
    
    try:
        from bot import (
            CharacterManagementView,
            UserCharacterManagementView,
            CreateCharacterModal,
            CreateUserCharacterModal,
            ConfirmCharacterDeleteView,
            ConfirmUserCharacterDeleteView
        )
        print("✓ CharacterManagementView imported successfully")
        print("✓ UserCharacterManagementView imported successfully")
        print("✓ CreateCharacterModal imported successfully")
        print("✓ CreateUserCharacterModal imported successfully")
        print("✓ ConfirmCharacterDeleteView imported successfully")
        print("✓ ConfirmUserCharacterDeleteView imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import character UI classes: {str(e)}")
        return False


async def test_character_views_initialization_async():
    """Test that character views can be initialized (async)"""
    from bot import (
        ConfigManager,
        CharacterManagementView,
        UserCharacterManagementView,
        CreateCharacterModal,
        CreateUserCharacterModal
    )
    
    # Create config manager
    test_config_path = "test_config_char_ui.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Add test characters
    config_mgr.add_character("test_ai", "Test AI", "A test AI character")
    config_mgr.add_user_character("test_user", "Test User", "A test user character")
    print("✓ Test characters added")
    
    # Test CharacterManagementView initialization
    try:
        view = CharacterManagementView(config_mgr, timeout=180)
        assert view is not None, "CharacterManagementView is None"
        assert view.timeout == 180, "CharacterManagementView timeout not set correctly"
        print("✓ CharacterManagementView initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize CharacterManagementView: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test UserCharacterManagementView initialization
    try:
        view = UserCharacterManagementView(config_mgr, timeout=180)
        assert view is not None, "UserCharacterManagementView is None"
        assert view.timeout == 180, "UserCharacterManagementView timeout not set correctly"
        print("✓ UserCharacterManagementView initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize UserCharacterManagementView: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test CreateCharacterModal initialization
    try:
        modal = CreateCharacterModal(config_mgr)
        assert modal is not None, "CreateCharacterModal is None"
        print("✓ CreateCharacterModal initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize CreateCharacterModal: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test CreateUserCharacterModal initialization
    try:
        modal = CreateUserCharacterModal(config_mgr)
        assert modal is not None, "CreateUserCharacterModal is None"
        print("✓ CreateUserCharacterModal initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize CreateUserCharacterModal: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_character_views_initialization():
    """Test that character views can be initialized"""
    print("\n" + "="*60)
    print("Testing Character View Initialization")
    print("="*60)
    
    return asyncio.run(test_character_views_initialization_async())


async def test_character_management_view_buttons_async():
    """Test that CharacterManagementView has correct buttons"""
    from bot import ConfigManager, CharacterManagementView
    
    test_config_path = "test_config_char_buttons.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    try:
        config_mgr = ConfigManager(test_config_path)
        
        # Add test characters
        config_mgr.add_character("char1", "Character 1", "Description 1")
        config_mgr.add_character("char2", "Character 2", "Description 2")
        
        view = CharacterManagementView(config_mgr)
        
        # Count components
        component_count = len(view.children)
        print(f"✓ CharacterManagementView has {component_count} interactive components")
        
        # Check for expected buttons/selects
        button_labels = [child.label for child in view.children if hasattr(child, 'label')]
        print(f"✓ Found buttons: {button_labels}")
        
        # Verify essential buttons exist
        assert "➕ Create Character" in button_labels, "Create Character button missing"
        print("✓ 'Create Character' button found")
        
        assert "👁️ View Details" in button_labels, "View Details button missing"
        print("✓ 'View Details' button found")
        
        assert "🗑️ Delete Character" in button_labels, "Delete button missing"
        print("✓ 'Delete Character' button found")
        
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


def test_character_management_view_buttons():
    """Test that CharacterManagementView has correct buttons"""
    print("\n" + "="*60)
    print("Testing Character Management View Buttons")
    print("="*60)
    
    return asyncio.run(test_character_management_view_buttons_async())


async def test_create_character_modal_fields_async():
    """Test that CreateCharacterModal has correct fields"""
    from bot import ConfigManager, CreateCharacterModal
    
    test_config_path = "test_config_char_modal.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    try:
        config_mgr = ConfigManager(test_config_path)
        modal = CreateCharacterModal(config_mgr)
        
        # Count fields
        field_count = len(modal.children)
        print(f"✓ CreateCharacterModal has {field_count} input field(s)")
        
        # Check field labels
        field_labels = [child.label for child in modal.children if hasattr(child, 'label')]
        print(f"✓ Field labels: {field_labels}")
        
        assert "Character Name (internal)" in field_labels, "Character Name field missing"
        print("✓ 'Character Name' field found")
        
        assert "Display Name" in field_labels, "Display Name field missing"
        print("✓ 'Display Name' field found")
        
        assert "System Prompt/Description" in field_labels, "Description field missing"
        print("✓ 'System Prompt/Description' field found")
        
        assert "Avatar URL (optional)" in field_labels, "Avatar URL field missing"
        print("✓ 'Avatar URL' field found")
        
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


def test_create_character_modal_fields():
    """Test that CreateCharacterModal has correct fields"""
    print("\n" + "="*60)
    print("Testing CreateCharacterModal Fields")
    print("="*60)
    
    return asyncio.run(test_create_character_modal_fields_async())


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Interactive Character Management - Test Suite")
    print("="*60)
    
    tests = [
        ("Character UI Imports", test_character_ui_imports),
        ("Character View Initialization", test_character_views_initialization),
        ("Character Management View Buttons", test_character_management_view_buttons),
        ("CreateCharacterModal Fields", test_create_character_modal_fields),
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
