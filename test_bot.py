#!/usr/bin/env python3
"""
Test Suite for Preset Bot

This script tests the core functionality of the bot without requiring
actual Discord or OpenAI API connections.
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any


def test_config_manager():
    """Test ConfigManager functionality"""
    print("\n" + "="*60)
    print("Testing ConfigManager")
    print("="*60)
    
    from bot import ConfigManager
    
    # Clean up any existing test config
    test_config_path = "test_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    # Initialize with test config
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Test Discord token
    config_mgr.set_discord_token("test_token_abc123")
    assert config_mgr.get_discord_token() == "test_token_abc123", "Discord token mismatch"
    print("✓ Discord token set and retrieved correctly")
    
    # Test OpenAI configuration
    config_mgr.set_openai_config("https://test.api.com/v1", "test_key_xyz789")
    openai_cfg = config_mgr.get_openai_config()
    assert openai_cfg["base_url"] == "https://test.api.com/v1", "OpenAI base URL mismatch"
    assert openai_cfg["api_key"] == "test_key_xyz789", "OpenAI API key mismatch"
    print("✓ OpenAI configuration set and retrieved correctly")
    
    # Test character management with new structure
    initial_chars = len(config_mgr.get_characters())
    config_mgr.add_character("testbot", "TestBot", "You are a friendly test bot.")
    config_mgr.add_character("helperbot", "HelperBot", "You are a helpful assistant bot.")
    
    characters = config_mgr.get_characters()
    assert len(characters) == initial_chars + 2, "Character count mismatch"
    
    char_names = [c["name"] for c in characters]
    assert "testbot" in char_names, "TestBot not found"
    assert "helperbot" in char_names, "HelperBot not found"
    print("✓ Characters added and retrieved correctly")
    
    # Test config persistence
    config_mgr2 = ConfigManager(test_config_path)
    assert config_mgr2.get_discord_token() == "test_token_abc123", "Config not persisted"
    print("✓ Configuration persisted to file")
    
    # Cleanup
    os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_ai_handler_init():
    """Test AIResponseHandler initialization"""
    print("\n" + "="*60)
    print("Testing AIResponseHandler")
    print("="*60)
    
    from bot import ConfigManager, AIResponseHandler
    
    # Clean up any existing test config
    test_config_path = "test_ai_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Test without API key (should not crash)
    ai_handler = AIResponseHandler(config_mgr)
    assert ai_handler.client is None, "Client should be None without API key"
    print("✓ AIResponseHandler handles missing API key gracefully")
    
    # Test with API key
    config_mgr.set_openai_config("https://test.api.com/v1", "test_key")
    ai_handler.update_client()
    assert ai_handler.client is not None, "Client should be initialized with API key"
    print("✓ AIResponseHandler client initialized with API key")
    
    # Cleanup
    os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_config_structure():
    """Test configuration file structure"""
    print("\n" + "="*60)
    print("Testing Configuration Structure")
    print("="*60)
    
    # Test template config
    with open("config_template.json", 'r') as f:
        template = json.load(f)
    
    assert "discord" in template, "Missing discord section"
    assert "token" in template["discord"], "Missing discord.token"
    assert "openai" in template, "Missing openai section"
    assert "base_url" in template["openai"], "Missing openai.base_url"
    assert "api_key" in template["openai"], "Missing openai.api_key"
    assert "characters" in template, "Missing characters section"
    assert isinstance(template["characters"], list), "Characters should be a list"
    print("✓ Configuration template structure is valid")
    
    # Test that default character exists
    assert len(template["characters"]) > 0, "Should have at least one default character"
    assert "name" in template["characters"][0], "Character missing name"
    # Support both old system_prompt and new description fields
    has_description = "description" in template["characters"][0] or "system_prompt" in template["characters"][0]
    assert has_description, "Character missing description/system_prompt"
    print("✓ Default character structure is valid")
    
    return True


def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*60)
    print("Testing Module Imports")
    print("="*60)
    
    try:
        import bot
        print("✓ bot.py imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import bot.py: {e}")
        return False
    
    try:
        from bot import ConfigManager, AIResponseHandler, PresetBot
        print("✓ Core classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import core classes: {e}")
        return False
    
    # Note: GUI might fail in headless environment
    try:
        import gui
        print("✓ gui.py imported successfully")
    except ImportError as e:
        print(f"⚠ gui.py import warning (expected in headless env): {e}")
    
    try:
        import start
        print("✓ start.py imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import start.py: {e}")
        return False
    
    try:
        import example_manual_send
        print("✓ example_manual_send.py imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import example_manual_send.py: {e}")
        return False
    
    return True


def test_requirements():
    """Test that requirements.txt is valid"""
    print("\n" + "="*60)
    print("Testing Requirements")
    print("="*60)
    
    with open("requirements.txt", 'r') as f:
        requirements = f.readlines()
    
    required_packages = ["discord.py", "openai", "python-dotenv"]
    for package in required_packages:
        found = any(package in req for req in requirements)
        if found:
            print(f"✓ {package} in requirements")
        else:
            print(f"✗ {package} missing from requirements")
            return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Preset Bot - Test Suite")
    print("="*60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Requirements File", test_requirements),
        ("Configuration Structure", test_config_structure),
        ("ConfigManager", test_config_manager),
        ("AIResponseHandler", test_ai_handler_init),
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
    success = main()
    sys.exit(0 if success else 1)
