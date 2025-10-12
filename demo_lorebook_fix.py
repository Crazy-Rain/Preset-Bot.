#!/usr/bin/env python3
"""
Demonstration script showing how the lorebook fix works.
This simulates the scenario where the GUI deactivates a lorebook
and the bot picks up the change without restarting.
"""

import os
import json
import asyncio
from bot import ConfigManager, AIResponseHandler


async def demonstrate_fix():
    """Demonstrate the lorebook dynamic reload fix"""
    print("\n" + "="*70)
    print("  LOREBOOK DYNAMIC RELOAD - DEMONSTRATION")
    print("="*70)
    
    # Setup
    test_config = "demo_lorebook_fix.json"
    if os.path.exists(test_config):
        os.remove(test_config)
    
    print("\n📝 SETUP: Creating test configuration...")
    config_mgr = ConfigManager(test_config)
    config_mgr.config["openai"] = {
        "base_url": "https://api.openai.com/v1",
        "api_key": "test-key",
        "model": "gpt-3.5-turbo"
    }
    config_mgr.save_config()
    
    # Create a lorebook with entries
    print("📚 Creating a lorebook with entries...")
    config_mgr.add_lorebook("fantasy_world", active=True)
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "This is a high-fantasy world with magic and dragons.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "Dragons are noble and wise creatures in this world.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    print("   ✓ Created 'fantasy_world' lorebook with 2 entries")
    print("   ✓ Status: ACTIVE")
    
    # Scenario 1: Active lorebook
    print("\n" + "-"*70)
    print("SCENARIO 1: User sends message with active lorebook")
    print("-"*70)
    
    message = "Tell me about dragons in this world"
    print(f"User message: \"{message}\"")
    
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"\n📥 Lorebook entries retrieved: {len(entries)}")
    for i, entry in enumerate(entries, 1):
        print(f"   {i}. {entry[:60]}...")
    
    print("\n✅ RESULT: Both constant and keyword-triggered entries included")
    print("   The AI response would include this lorebook context")
    
    # Scenario 2: GUI deactivates lorebook (simulated)
    print("\n" + "-"*70)
    print("SCENARIO 2: GUI deactivates the lorebook (bot still running)")
    print("-"*70)
    
    print("🖱️  User clicks 'Deactivate' in GUI for 'fantasy_world'")
    print("💾 GUI saves config.json with lorebook.active = false")
    
    # Simulate GUI action - directly modify the config file
    with open(test_config, 'r') as f:
        config_data = json.load(f)
    config_data["lorebooks"][0]["active"] = False
    with open(test_config, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print("   ✓ Config file updated on disk")
    
    # Scenario 3: WITHOUT the fix (old behavior)
    print("\n" + "-"*70)
    print("SCENARIO 3: WITHOUT fix - Bot uses cached config")
    print("-"*70)
    
    print("🤖 Bot's in-memory config is NOT reloaded")
    print(f"   Cached lorebook status: {config_mgr.get_lorebooks()[0]['active']}")
    
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"\n📥 Lorebook entries retrieved: {len(entries)}")
    
    print("\n❌ PROBLEM: Entries still retrieved even though GUI deactivated them!")
    print("   User expects no lorebook context, but it's still included")
    
    # Scenario 4: WITH the fix (new behavior)
    print("\n" + "-"*70)
    print("SCENARIO 4: WITH fix - Bot reloads config before using lorebooks")
    print("-"*70)
    
    print("🤖 Bot calls reload_config() before accessing lorebooks")
    config_mgr.reload_config()
    print(f"   Reloaded lorebook status: {config_mgr.get_lorebooks()[0]['active']}")
    
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"\n📥 Lorebook entries retrieved: {len(entries)}")
    
    print("\n✅ FIXED: No entries retrieved - deactivation is respected!")
    print("   User's GUI changes take effect immediately")
    
    # Where the fix is applied
    print("\n" + "="*70)
    print("  WHERE THE FIX IS APPLIED")
    print("="*70)
    
    print("""
The fix adds reload_config() calls to:

1. AIResponseHandler.get_ai_response() method
   - Called every time the bot generates an AI response
   - Ensures lorebook states are current before including entries
   
2. !lorebook command handler
   - Called when users run !lorebook list, show, etc.
   - Ensures displayed lorebook states are current
   
This means:
✓ No bot restart needed when GUI changes lorebooks
✓ Deactivated lorebooks immediately stop contributing to responses
✓ Activated lorebooks immediately start contributing to responses
✓ !lorebook commands show current state, not cached state
""")
    
    # Cleanup
    os.remove(test_config)
    print("\n✓ Demonstration complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demonstrate_fix())
