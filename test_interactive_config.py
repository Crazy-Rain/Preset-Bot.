#!/usr/bin/env python3
"""
Test Suite for Interactive Configuration Feature

This script tests the Discord-based configuration UI.
"""

import os
import sys
import asyncio


def test_config_view_imports():
    """Test that the config UI views can be imported"""
    print("\n" + "="*60)
    print("Testing Config UI Imports")
    print("="*60)
    
    try:
        from bot import ConfigMenuView, OpenAIConfigModal
        print("✓ ConfigMenuView imported successfully")
        print("✓ OpenAIConfigModal imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import config UI classes: {str(e)}")
        return False


async def test_config_view_initialization_async():
    """Test that config views can be initialized (async)"""
    from bot import ConfigManager, ConfigMenuView, OpenAIConfigModal
    
    # Create config manager
    test_config_path = "test_config_ui.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Test ConfigMenuView initialization
    try:
        view = ConfigMenuView(config_mgr, timeout=180)
        assert view is not None, "ConfigMenuView is None"
        assert view.timeout == 180, "ConfigMenuView timeout not set correctly"
        print("✓ ConfigMenuView initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize ConfigMenuView: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Test OpenAIConfigModal initialization
    try:
        modal = OpenAIConfigModal(config_mgr)
        assert modal is not None, "OpenAIConfigModal is None"
        print("✓ OpenAIConfigModal initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize OpenAIConfigModal: {str(e)}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_config_view_initialization():
    """Test that config views can be initialized"""
    print("\n" + "="*60)
    print("Testing Config View Initialization")
    print("="*60)
    
    return asyncio.run(test_config_view_initialization_async())


async def test_config_view_buttons_async():
    """Test that config view has the expected buttons (async)"""
    from bot import ConfigManager, ConfigMenuView
    
    # Create config manager
    test_config_path = "test_config_ui_buttons.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    view = ConfigMenuView(config_mgr)
    
    # Check that view has buttons
    assert hasattr(view, 'children'), "View has no children (buttons)"
    assert len(view.children) > 0, "View has no buttons"
    print(f"✓ ConfigMenuView has {len(view.children)} interactive components")
    
    # Check button labels
    button_labels = [child.label for child in view.children if hasattr(child, 'label')]
    expected_labels = ["🔧 OpenAI Config", "🤖 Characters", "👥 User Characters", 
                      "⚙️ Bot Settings", "📚 Lorebooks", "🎯 Presets", "❌ Close"]
    
    for label in expected_labels:
        assert label in button_labels, f"Expected button '{label}' not found"
        print(f"✓ Button '{label}' found")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_config_view_buttons():
    """Test that config view has the expected buttons"""
    print("\n" + "="*60)
    print("Testing Config View Buttons")
    print("="*60)
    
    return asyncio.run(test_config_view_buttons_async())


async def test_openai_modal_fields_async():
    """Test that OpenAI modal has the expected input fields (async)"""
    from bot import ConfigManager, OpenAIConfigModal
    
    # Create config manager
    test_config_path = "test_config_ui_modal.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    modal = OpenAIConfigModal(config_mgr)
    
    # Check that modal has input fields
    assert hasattr(modal, 'children'), "Modal has no children (input fields)"
    assert len(modal.children) > 0, "Modal has no input fields"
    print(f"✓ OpenAIConfigModal has {len(modal.children)} input fields")
    
    # Check field labels
    field_labels = [child.label for child in modal.children if hasattr(child, 'label')]
    expected_labels = ["Base URL", "API Key", "Model (optional)"]
    
    for label in expected_labels:
        assert label in field_labels, f"Expected field '{label}' not found"
        print(f"✓ Field '{label}' found")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_openai_modal_fields():
    """Test that OpenAI modal has the expected input fields"""
    print("\n" + "="*60)
    print("Testing OpenAI Modal Fields")
    print("="*60)
    
    return asyncio.run(test_openai_modal_fields_async())


def main():
    """Run all tests"""
    print("="*60)
    print("  Interactive Configuration - Test Suite")
    print("="*60)
    
    tests = [
        ("Config UI Imports", test_config_view_imports),
        ("Config View Initialization", test_config_view_initialization),
        ("Config View Buttons", test_config_view_buttons),
        ("OpenAI Modal Fields", test_openai_modal_fields),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"\n✅ PASS - {test_name}")
            else:
                failed += 1
                print(f"\n❌ FAIL - {test_name}")
        except Exception as e:
            failed += 1
            print(f"\n❌ FAIL - {test_name}")
            print(f"Error: {str(e)}")
            import traceback
            print(traceback.format_exc())
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("="*60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
