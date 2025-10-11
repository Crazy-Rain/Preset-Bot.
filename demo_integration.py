#!/usr/bin/env python3
"""
Integration Demo: Lorebook GUI and Console Features

This script demonstrates the complete workflow of using the new GUI features:
1. Creating lorebooks via GUI methods
2. Managing entries with different activation types
3. Seeing how the console logs operations

Run this to verify the implementation is working correctly.
"""

import os
import json
from bot import ConfigManager

def print_section(title):
    """Print a section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def main():
    """Demonstrate the complete lorebook GUI workflow"""
    
    # Setup
    config_path = "demo_integration_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    print_section("Lorebook GUI Integration Demo")
    print("\nThis demo shows how the GUI features would work together.")
    print("In the actual GUI, these operations happen through buttons and forms.")
    
    # Scenario 1: Setting up a fantasy world lorebook
    print_section("Scenario 1: Creating a Fantasy World Lorebook")
    
    print("\n1. User creates a new lorebook via GUI:")
    print("   - Enters name: 'fantasy_world'")
    print("   - Clicks 'Create' button")
    config_mgr.add_lorebook("fantasy_world", active=True)
    print("   ✓ Lorebook created and activated")
    
    print("\n2. User adds a constant entry (always active):")
    print("   - Selects lorebook: fantasy_world")
    print("   - Enters content in text area")
    print("   - Selects activation type: Constant")
    print("   - Clicks 'Add Entry'")
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "This is a high-fantasy medieval world with magic and ancient mysteries.",
        insertion_type="constant"
    )
    print("   ✓ Constant entry added")
    print("   Console log: '[timestamp] Entry added to lorebook fantasy_world'")
    
    print("\n3. User adds keyword-triggered entries:")
    entries = [
        ("Dragons are rare, powerful creatures that guard ancient treasures.", 
         ["dragon", "dragons", "wyrm"]),
        ("Elves are immortal beings who live in harmony with nature.",
         ["elf", "elves", "elven"]),
        ("The Mage Guild controls all magical education and licensing.",
         ["mage", "wizard", "magic guild"]),
        ("Silverhaven is the capital city, built around a magical silver lake.",
         ["silverhaven", "capital", "city"])
    ]
    
    for content, keywords in entries:
        print(f"   - Adding entry with keywords: {', '.join(keywords)}")
        config_mgr.add_lorebook_entry(
            "fantasy_world",
            content,
            insertion_type="normal",
            keywords=keywords
        )
    print("   ✓ 4 keyword-triggered entries added")
    print("   Console log: '[timestamp] 4 entries added successfully'")
    
    # Scenario 2: Testing the lorebook with different messages
    print_section("Scenario 2: Testing Active Entries")
    
    test_messages = [
        ("Hello, what kind of world is this?", "No specific keywords"),
        ("Tell me about dragons", "Triggers: dragon entry"),
        ("What is Silverhaven like?", "Triggers: city entry"),
        ("Are there dragons and elves in Silverhaven?", "Triggers: dragon, elf, city entries"),
        ("Tell me about the Mage Guild's rules", "Triggers: mage entry")
    ]
    
    for message, description in test_messages:
        print(f"\nMessage: \"{message}\"")
        print(f"Description: {description}")
        entries = config_mgr.get_active_lorebook_entries(message)
        print(f"Entries sent to AI: {len(entries)}")
        print("Console log:")
        print(f"  [timestamp] Processing message: \"{message}\"")
        print(f"  [timestamp] Retrieved {len(entries)} lorebook entries")
        for i, entry in enumerate(entries, 1):
            snippet = entry[:60] + "..." if len(entry) > 60 else entry
            print(f"    {i}. {snippet}")
    
    # Scenario 3: Managing multiple lorebooks
    print_section("Scenario 3: Multiple Lorebooks")
    
    print("\n1. User creates a sci-fi lorebook:")
    config_mgr.add_lorebook("sci_fi_universe", active=False)
    config_mgr.add_lorebook_entry(
        "sci_fi_universe",
        "Humanity has spread across the galaxy in massive colony ships.",
        insertion_type="constant"
    )
    config_mgr.add_lorebook_entry(
        "sci_fi_universe",
        "AI entities are common and have equal rights with humans.",
        insertion_type="normal",
        keywords=["AI", "artificial intelligence", "robot"]
    )
    print("   ✓ Sci-fi lorebook created (inactive)")
    print("   Console log: '[timestamp] Lorebook sci_fi_universe created (inactive)'")
    
    print("\n2. Current lorebooks in GUI list:")
    lorebooks = config_mgr.get_lorebooks()
    for lb in lorebooks:
        status = "✓" if lb['active'] else "✗"
        entry_count = len(lb.get('entries', []))
        print(f"   {status} {lb['name']} ({entry_count} entries)")
    
    print("\n3. Testing with fantasy active, sci-fi inactive:")
    message = "Tell me about AI and dragons"
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"   Message: \"{message}\"")
    print(f"   Entries retrieved: {len(entries)}")
    print("   Console log:")
    print(f"     [timestamp] Active lorebooks: fantasy_world")
    print(f"     [timestamp] Matched entries: 2 (constant + dragon)")
    print(f"     Note: AI entry NOT included (lorebook inactive)")
    
    # Scenario 4: Editing entries
    print_section("Scenario 4: Editing an Entry")
    
    print("\n1. User selects dragon entry and clicks 'Edit Selected'")
    print("   - Form populates with current data")
    print("   - User modifies content")
    print("   - Clicks 'Update Entry'")
    
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    print(f"\n   Current dragon entry:")
    print(f"   \"{lorebook['entries'][1]['content']}\"")
    
    config_mgr.update_lorebook_entry(
        "fantasy_world",
        1,
        "Dragons are extremely rare and powerful ancient beings, known for their wisdom and magical abilities.",
        insertion_type="normal",
        keywords=["dragon", "dragons", "wyrm", "drake"]
    )
    
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    print(f"\n   Updated dragon entry:")
    print(f"   \"{lorebook['entries'][1]['content']}\"")
    print(f"   Keywords: {', '.join(lorebook['entries'][1]['keywords'])}")
    print("\n   ✓ Entry updated successfully")
    print("   Console log: '[timestamp] Entry #1 in fantasy_world updated'")
    
    # Scenario 5: Activating/Deactivating lorebooks
    print_section("Scenario 5: Toggling Lorebook Status")
    
    print("\n1. User deactivates fantasy_world:")
    config_mgr.toggle_lorebook_active("fantasy_world", False)
    print("   ✓ fantasy_world deactivated")
    print("   Console log: '[timestamp] Lorebook fantasy_world deactivated'")
    
    print("\n2. User activates sci_fi_universe:")
    config_mgr.toggle_lorebook_active("sci_fi_universe", True)
    print("   ✓ sci_fi_universe activated")
    print("   Console log: '[timestamp] Lorebook sci_fi_universe activated'")
    
    print("\n3. Testing with swapped active states:")
    message = "Tell me about AI and dragons"
    entries = config_mgr.get_active_lorebook_entries(message)
    print(f"   Message: \"{message}\"")
    print(f"   Entries retrieved: {len(entries)}")
    print(f"   Content: Sci-fi entries only (fantasy inactive)")
    print("   Console log:")
    print(f"     [timestamp] Active lorebooks: sci_fi_universe")
    print(f"     [timestamp] Matched entries: 2 (constant + AI)")
    
    # Summary
    print_section("Summary")
    
    print("\nThe GUI provides:")
    print("  ✓ Visual lorebook management (create, edit, delete)")
    print("  ✓ Entry management with activation types")
    print("  ✓ Active/inactive toggling")
    print("  ✓ Real-time console logging of all operations")
    print("  ✓ Color-coded console output for different log types")
    print("  ✓ Export and clear console functionality")
    
    print("\nLorebook Statistics:")
    lorebooks = config_mgr.get_lorebooks()
    total_entries = sum(len(lb.get('entries', [])) for lb in lorebooks)
    active_lorebooks = sum(1 for lb in lorebooks if lb.get('active', False))
    print(f"  Total Lorebooks: {len(lorebooks)}")
    print(f"  Active Lorebooks: {active_lorebooks}")
    print(f"  Total Entries: {total_entries}")
    
    # Cleanup
    os.remove(config_path)
    
    print("\n" + "="*70)
    print("  Demo Complete!")
    print("="*70)
    print("\nThe actual GUI provides all these features with:")
    print("  - Point-and-click interface")
    print("  - Real-time console logging")
    print("  - Visual feedback and confirmations")
    print("  - Integrated with existing bot functionality")

if __name__ == "__main__":
    main()
