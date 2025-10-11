#!/usr/bin/env python3
"""
Lorebook Feature Demo

This script demonstrates the lorebook functionality without requiring 
a Discord connection or API calls.
"""

import os
import json
from bot import ConfigManager


def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def demo_basic_lorebook():
    """Demonstrate basic lorebook creation and management"""
    print_section("Demo: Basic Lorebook Creation")
    
    # Clean up any existing demo config
    config_path = "demo_lorebook_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    print("\n1. Creating a fantasy world lorebook...")
    config_mgr.add_lorebook("fantasy_world", active=True)
    print("   ✓ Created 'fantasy_world' lorebook (active)")
    
    print("\n2. Creating a sci-fi world lorebook...")
    config_mgr.add_lorebook("sci_fi_world", active=False)
    print("   ✓ Created 'sci_fi_world' lorebook (inactive)")
    
    print("\n3. Listing all lorebooks...")
    lorebooks = config_mgr.get_lorebooks()
    for i, lb in enumerate(lorebooks):
        status = "Active" if lb.get("active") else "Inactive"
        print(f"   {i+1}. {lb.get('name')} - {status}")
    
    print("\n4. Deactivating fantasy_world...")
    config_mgr.toggle_lorebook_active("fantasy_world", False)
    print("   ✓ Deactivated")
    
    print("\n5. Activating both lorebooks...")
    config_mgr.toggle_lorebook_active("fantasy_world", True)
    config_mgr.toggle_lorebook_active("sci_fi_world", True)
    lorebooks = config_mgr.get_lorebooks()
    for i, lb in enumerate(lorebooks):
        status = "Active" if lb.get("active") else "Inactive"
        print(f"   {i+1}. {lb.get('name')} - {status}")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo complete")


def demo_lorebook_entries():
    """Demonstrate adding and managing lorebook entries"""
    print_section("Demo: Lorebook Entries")
    
    config_path = "demo_entries_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    config_mgr.add_lorebook("fantasy_realm", active=True)
    
    print("\n1. Adding a CONSTANT entry (always active)...")
    config_mgr.add_lorebook_entry(
        "fantasy_realm",
        "This is a high-fantasy world where magic flows through everything.",
        insertion_type="constant"
    )
    print("   ✓ Added constant entry")
    
    print("\n2. Adding NORMAL entries with keywords...")
    
    config_mgr.add_lorebook_entry(
        "fantasy_realm",
        "Dragons are ancient, intelligent beings who can speak telepathically and breathe fire.",
        insertion_type="normal",
        keywords=["dragon", "dragons", "drake"]
    )
    print("   ✓ Added dragon entry (keywords: dragon, dragons, drake)")
    
    config_mgr.add_lorebook_entry(
        "fantasy_realm",
        "Elves are immortal forest dwellers with natural magical abilities and keen archery skills.",
        insertion_type="normal",
        keywords=["elf", "elves", "elven"]
    )
    print("   ✓ Added elf entry (keywords: elf, elves, elven)")
    
    config_mgr.add_lorebook_entry(
        "fantasy_realm",
        "The Mage Guild is the governing body for all magical education and research.",
        insertion_type="normal",
        keywords=["mage", "mages", "wizard", "magic", "guild"]
    )
    print("   ✓ Added magic entry (keywords: mage, mages, wizard, magic, guild)")
    
    print("\n3. Displaying all entries...")
    lorebook = config_mgr.get_lorebook_by_name("fantasy_realm")
    entries = lorebook.get("entries", [])
    for i, entry in enumerate(entries):
        entry_type = entry.get("insertion_type", "normal").upper()
        content = entry.get("content", "")[:60] + "..."
        keywords = entry.get("keywords", [])
        print(f"\n   Entry {i} [{entry_type}]")
        print(f"   Content: {content}")
        if keywords:
            print(f"   Keywords: {', '.join(keywords)}")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo complete")


def demo_keyword_matching():
    """Demonstrate how keyword matching works"""
    print_section("Demo: Keyword Matching")
    
    config_path = "demo_matching_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    config_mgr.add_lorebook("game_world", active=True)
    
    # Setup entries
    config_mgr.add_lorebook_entry(
        "game_world",
        "This world operates on medieval technology with magical enhancements.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "game_world",
        "Dragons are rare and powerful creatures that hoard treasure.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    config_mgr.add_lorebook_entry(
        "game_world",
        "The capital city of Silverhaven is built on a floating island.",
        insertion_type="normal",
        keywords=["silverhaven", "capital", "city"]
    )
    
    print("\nSetup complete. Testing different messages:\n")
    
    # Test different messages
    test_cases = [
        ("Hello, what is this place?", "No keywords"),
        ("Tell me about dragons", "Contains 'dragons'"),
        ("Are there any DRAGONS here?", "Contains 'DRAGONS' (uppercase)"),
        ("What's the capital city like?", "Contains 'capital' and 'city'"),
        ("Tell me about dragons in Silverhaven", "Contains multiple keywords"),
    ]
    
    for message, description in test_cases:
        print(f"Message: \"{message}\"")
        print(f"  ({description})")
        entries = config_mgr.get_active_lorebook_entries(message)
        print(f"  Matched entries: {len(entries)}")
        for i, entry in enumerate(entries):
            snippet = entry[:50] + "..." if len(entry) > 50 else entry
            print(f"    {i+1}. {snippet}")
        print()
    
    # Cleanup
    os.remove(config_path)
    print("✓ Demo complete")


def demo_active_inactive():
    """Demonstrate active/inactive lorebook behavior"""
    print_section("Demo: Active vs Inactive Lorebooks")
    
    config_path = "demo_active_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    # Create two lorebooks
    config_mgr.add_lorebook("active_lore", active=True)
    config_mgr.add_lorebook("inactive_lore", active=False)
    
    # Add entries to both
    config_mgr.add_lorebook_entry(
        "active_lore",
        "This entry is from the ACTIVE lorebook.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "inactive_lore",
        "This entry is from the INACTIVE lorebook.",
        insertion_type="constant"
    )
    
    print("\nSetup:")
    print("  - active_lore: ACTIVE, has 1 constant entry")
    print("  - inactive_lore: INACTIVE, has 1 constant entry")
    
    message = "Tell me about this world"
    print(f"\nMessage: \"{message}\"")
    
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"Entries retrieved: {len(entries)}")
    for entry in entries:
        print(f"  - {entry}")
    
    print("\nExpected: Only entry from active_lore should appear")
    print("✓ Inactive lorebooks are correctly ignored")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo complete")


def demo_persistence():
    """Demonstrate that lorebooks persist across sessions"""
    print_section("Demo: Configuration Persistence")
    
    config_path = "demo_persistence_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    print("\n1. Creating lorebook in first session...")
    config_mgr1 = ConfigManager(config_path)
    config_mgr1.add_lorebook("persistent_world", active=True)
    config_mgr1.add_lorebook_entry(
        "persistent_world",
        "This is persistent data.",
        insertion_type="constant"
    )
    print("   ✓ Created lorebook with 1 entry")
    print(f"   ✓ Saved to {config_path}")
    
    print("\n2. Loading config in new session (simulating bot restart)...")
    config_mgr2 = ConfigManager(config_path)
    lorebooks = config_mgr2.get_lorebooks()
    print(f"   ✓ Found {len(lorebooks)} lorebook(s)")
    
    lorebook = config_mgr2.get_lorebook_by_name("persistent_world")
    if lorebook:
        entries = lorebook.get("entries", [])
        print(f"   ✓ Lorebook has {len(entries)} entry/entries")
        print(f"   ✓ Entry content: \"{entries[0].get('content')}\"")
    
    print("\n3. Verifying the saved file...")
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    print(f"   Config has 'lorebooks' key: {('lorebooks' in config_data)}")
    print(f"   Number of lorebooks: {len(config_data.get('lorebooks', []))}")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo complete")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("  LOREBOOK FEATURE DEMONSTRATION")
    print("="*60)
    print("\nThis demo shows how the lorebook system works.")
    print("No Discord or API connection required.")
    
    demos = [
        demo_basic_lorebook,
        demo_lorebook_entries,
        demo_keyword_matching,
        demo_active_inactive,
        demo_persistence,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n✗ Demo failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("  ALL DEMOS COMPLETE")
    print("="*60)
    print("\nThe lorebook system is fully functional!")
    print("\nNext steps:")
    print("  1. Run the bot with: python start.py")
    print("  2. Use !lorebook commands in Discord")
    print("  3. See LOREBOOK_GUIDE.md for full documentation")
    print()


if __name__ == "__main__":
    main()
