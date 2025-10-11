#!/usr/bin/env python3
"""
Test Lorebook Integration with AI Response
"""

import os
import json
from bot import ConfigManager, AIResponseHandler


def test_lorebook_ai_integration():
    """Test that lorebook entries are properly integrated into AI responses"""
    print("\n" + "="*60)
    print("Testing Lorebook AI Integration")
    print("="*60)
    
    # Create test config
    test_config = "test_integration.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    config_mgr = ConfigManager(test_config)
    
    # Set up basic OpenAI config (won't actually call API)
    config_mgr.set_openai_config("https://api.openai.com/v1", "test-key")
    
    # Create lorebook with entries
    config_mgr.add_lorebook("test_world", active=True)
    config_mgr.add_lorebook_entry(
        "test_world",
        "The world is filled with magic.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "test_world",
        "Dragons are friendly and wise creatures.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    
    # Test that get_active_lorebook_entries works
    message1 = "Hello world"
    entries1 = config_mgr.get_active_lorebook_entries(message1)
    assert len(entries1) == 1, f"Expected 1 entry, got {len(entries1)}"
    assert "magic" in entries1[0], "Constant entry not found"
    print("✓ Constant entry retrieved for normal message")
    
    message2 = "Tell me about dragons"
    entries2 = config_mgr.get_active_lorebook_entries(message2)
    assert len(entries2) == 2, f"Expected 2 entries, got {len(entries2)}"
    assert any("magic" in e for e in entries2), "Constant entry not found"
    assert any("Dragons are friendly" in e for e in entries2), "Dragon entry not found"
    print("✓ Both constant and keyword-triggered entries retrieved")
    
    # Test with inactive lorebook
    config_mgr.toggle_lorebook_active("test_world", False)
    message3 = "Tell me about dragons"
    entries3 = config_mgr.get_active_lorebook_entries(message3)
    assert len(entries3) == 0, f"Expected 0 entries from inactive lorebook, got {len(entries3)}"
    print("✓ Inactive lorebook entries not retrieved")
    
    # Test case insensitivity
    config_mgr.toggle_lorebook_active("test_world", True)
    message4 = "Tell me about DRAGONS"
    entries4 = config_mgr.get_active_lorebook_entries(message4)
    assert len(entries4) == 2, f"Expected 2 entries (case insensitive), got {len(entries4)}"
    print("✓ Keyword matching is case-insensitive")
    
    # Cleanup
    os.remove(test_config)
    print("✓ Test cleanup complete")
    
    return True


def main():
    """Run integration tests"""
    print("\n" + "="*60)
    print("  Lorebook Integration - Test Suite")
    print("="*60)
    
    try:
        result = test_lorebook_ai_integration()
        print("\n" + "="*60)
        print("  Test Summary")
        print("="*60)
        if result:
            print("✅ PASS - Lorebook AI Integration")
        else:
            print("❌ FAIL - Lorebook AI Integration")
        print("="*60)
        return result
    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
