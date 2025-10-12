#!/usr/bin/env python3
"""
Test that lorebook changes are dynamically reloaded when generating AI responses.
This test verifies the fix for the issue where deactivated lorebooks were still being used.
"""

import os
import json
import asyncio
from bot import ConfigManager, AIResponseHandler


async def test_lorebook_dynamic_reload():
    """Test that lorebook state changes are picked up dynamically"""
    print("\n" + "="*60)
    print("Testing Dynamic Lorebook Reload in AI Responses")
    print("="*60)
    
    # Create test config
    test_config = "test_dynamic_reload.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    # Initialize config manager
    config_mgr = ConfigManager(test_config)
    
    # Set up minimal OpenAI config (won't actually call API in this test)
    config_mgr.config["openai"] = {
        "base_url": "https://api.openai.com/v1",
        "api_key": "test-key",
        "model": "gpt-3.5-turbo"
    }
    config_mgr.save_config()
    
    # Create an active lorebook with entries
    config_mgr.add_lorebook("test_world", active=True)
    config_mgr.add_lorebook_entry(
        "test_world",
        "This is a test world constant entry.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "test_world",
        "Dragons exist in this world.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    
    # Create AI handler
    ai_handler = AIResponseHandler(config_mgr)
    
    # Test 1: Verify entries are retrieved when lorebook is active
    print("\nTest 1: Active lorebook entries should be retrieved")
    message = "Tell me about dragons"
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, f"Expected 2 entries (constant + dragon), got {len(entries)}"
    assert any("test world constant" in e for e in entries), "Missing constant entry"
    assert any("Dragons exist" in e for e in entries), "Missing dragon entry"
    print("✓ Active lorebook entries retrieved correctly")
    
    # Test 2: Deactivate lorebook EXTERNALLY (simulating GUI change)
    print("\nTest 2: Deactivate lorebook externally (simulating GUI save)")
    # Directly modify the config file (simulating what GUI does)
    with open(test_config, 'r') as f:
        config_data = json.load(f)
    config_data["lorebooks"][0]["active"] = False
    with open(test_config, 'w') as f:
        json.dump(config_data, f, indent=2)
    print("✓ Lorebook deactivated in config file")
    
    # Test 3: Verify that WITHOUT reload, old cached data is used
    print("\nTest 3: Without reload, cached config should still show active")
    # config_mgr still has cached version where lorebook is active
    cached_lorebooks = config_mgr.get_lorebooks()
    assert cached_lorebooks[0]["active"] == True, "Cache should still show active"
    print("✓ Cached config still shows lorebook as active (expected)")
    
    # Test 4: Reload config and verify inactive lorebook is not used
    print("\nTest 4: After reload, lorebook should be inactive")
    config_mgr.reload_config()
    reloaded_lorebooks = config_mgr.get_lorebooks()
    assert reloaded_lorebooks[0]["active"] == False, "After reload, should be inactive"
    print("✓ After reload, lorebook correctly shows as inactive")
    
    # Test 5: Verify inactive lorebook entries are NOT retrieved
    print("\nTest 5: Inactive lorebook entries should NOT be retrieved")
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 0, f"Expected 0 entries from inactive lorebook, got {len(entries)}"
    print("✓ Inactive lorebook entries correctly excluded")
    
    # Test 6: Simulate the fix - get_ai_response should auto-reload
    print("\nTest 6: Simulating external lorebook activation")
    # Re-activate the lorebook externally
    with open(test_config, 'r') as f:
        config_data = json.load(f)
    config_data["lorebooks"][0]["active"] = True
    with open(test_config, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    # The config_manager still has cached inactive state
    # But get_ai_response should call reload_config() internally
    # We can't easily test the full get_ai_response without API, but we can verify
    # that calling reload_config() before get_active_lorebook_entries works
    
    # First verify cache is still inactive
    assert config_mgr.get_lorebooks()[0]["active"] == False, "Cache should still be inactive"
    
    # Now simulate what get_ai_response does: reload then get entries
    config_mgr.reload_config()
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, f"After reload, should get 2 entries, got {len(entries)}"
    print("✓ Reloading config before getting entries picks up external changes")
    
    # Cleanup
    os.remove(test_config)
    print("\n✓ Test cleanup complete")
    
    return True


async def test_multiple_lorebook_states():
    """Test that multiple lorebooks with different states are handled correctly"""
    print("\n" + "="*60)
    print("Testing Multiple Lorebooks with Different States")
    print("="*60)
    
    test_config = "test_multiple_states.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Create multiple lorebooks with different states
    config_mgr.add_lorebook("world1", active=True)
    config_mgr.add_lorebook("world2", active=False)
    config_mgr.add_lorebook("world3", active=True)
    
    # Add entries to each
    config_mgr.add_lorebook_entry("world1", "World 1 entry", insertion_type="constant")
    config_mgr.add_lorebook_entry("world2", "World 2 entry", insertion_type="constant")
    config_mgr.add_lorebook_entry("world3", "World 3 entry", insertion_type="constant")
    
    # Test initial state
    message = "test"
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, f"Expected 2 entries (world1 + world3), got {len(entries)}"
    assert any("World 1" in e for e in entries), "Missing world1 entry"
    assert any("World 3" in e for e in entries), "Missing world3 entry"
    assert not any("World 2" in e for e in entries), "World2 entry should not appear"
    print("✓ Multiple lorebooks filtered correctly by active state")
    
    # Externally change states
    with open(test_config, 'r') as f:
        config_data = json.load(f)
    config_data["lorebooks"][0]["active"] = False  # Deactivate world1
    config_data["lorebooks"][1]["active"] = True   # Activate world2
    with open(test_config, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    # Reload and test
    config_mgr.reload_config()
    entries = config_mgr.get_active_lorebook_entries(message)
    assert len(entries) == 2, f"Expected 2 entries (world2 + world3), got {len(entries)}"
    assert not any("World 1" in e for e in entries), "World1 should not appear"
    assert any("World 2" in e for e in entries), "Missing world2 entry"
    assert any("World 3" in e for e in entries), "Missing world3 entry"
    print("✓ Lorebook state changes correctly applied after reload")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Lorebook Dynamic Reload - Test Suite")
    print("="*60)
    
    tests = [
        ("Dynamic Reload", test_lorebook_dynamic_reload),
        ("Multiple States", test_multiple_lorebook_states),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = asyncio.run(test_func())
            results.append((name, result))
        except Exception as e:
            print(f"❌ FAILED - {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
