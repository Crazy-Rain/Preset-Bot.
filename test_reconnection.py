#!/usr/bin/env python3
"""
Test Suite for Bot Reconnection Feature

This script tests the automatic reconnection functionality.
"""

import os
import sys
import json


def test_reconnect_config():
    """Test reconnection configuration"""
    print("\n" + "="*60)
    print("Testing Reconnection Configuration")
    print("="*60)
    
    from bot import ConfigManager
    
    # Clean up any existing test config
    test_config_path = "test_reconnect_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    # Initialize with test config
    config_mgr = ConfigManager(test_config_path)
    print("✓ ConfigManager initialized")
    
    # Test reconnection config retrieval
    reconnect_config = config_mgr.get_reconnect_config()
    assert "enabled" in reconnect_config, "Missing 'enabled' key in reconnect config"
    assert "max_retries" in reconnect_config, "Missing 'max_retries' key in reconnect config"
    assert "base_delay" in reconnect_config, "Missing 'base_delay' key in reconnect config"
    assert "max_delay" in reconnect_config, "Missing 'max_delay' key in reconnect config"
    print("✓ Reconnection config has all required fields")
    
    # Test default values
    assert reconnect_config["enabled"] == True, "Default enabled should be True"
    assert reconnect_config["max_retries"] == 10, "Default max_retries should be 10"
    assert reconnect_config["base_delay"] == 5, "Default base_delay should be 5"
    assert reconnect_config["max_delay"] == 300, "Default max_delay should be 300"
    print("✓ Default reconnection values are correct")
    
    # Test that config is saved correctly
    config_mgr.save_config()
    assert os.path.exists(test_config_path), "Config file was not created"
    print("✓ Reconnection configuration persisted to file")
    
    # Verify saved config has reconnection settings
    with open(test_config_path, 'r') as f:
        saved_config = json.load(f)
    
    assert "discord" in saved_config, "Missing 'discord' key in saved config"
    assert "reconnect" in saved_config["discord"], "Missing 'reconnect' key in discord config"
    print("✓ Saved configuration contains reconnection settings")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    print("✓ Test cleanup complete")
    
    return True


def test_config_template():
    """Test that config template includes reconnection settings"""
    print("\n" + "="*60)
    print("Testing Configuration Template")
    print("="*60)
    
    template_path = "config_template.json"
    assert os.path.exists(template_path), "config_template.json not found"
    print("✓ Configuration template file exists")
    
    with open(template_path, 'r') as f:
        template = json.load(f)
    
    assert "discord" in template, "Missing 'discord' key in template"
    assert "reconnect" in template["discord"], "Missing 'reconnect' key in discord config"
    print("✓ Template contains reconnection settings")
    
    reconnect = template["discord"]["reconnect"]
    assert "enabled" in reconnect, "Missing 'enabled' in reconnect config"
    assert "max_retries" in reconnect, "Missing 'max_retries' in reconnect config"
    assert "base_delay" in reconnect, "Missing 'base_delay' in reconnect config"
    assert "max_delay" in reconnect, "Missing 'max_delay' in reconnect config"
    print("✓ Template has all required reconnection fields")
    
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("  Bot Reconnection - Test Suite")
    print("="*60)
    
    tests = [
        ("Reconnection Configuration", test_reconnect_config),
        ("Configuration Template", test_config_template),
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
