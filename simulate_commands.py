#!/usr/bin/env python3
"""
Command Simulation - Shows what bot commands would do

This simulates the bot commands without requiring Discord.
Shows the expected behavior of each lorebook command.
"""

import os
import json
from bot import ConfigManager


def print_command(cmd):
    """Print a command in a Discord-like format"""
    print(f"\n> {cmd}")
    print("-" * 60)


def simulate_commands():
    """Simulate a series of lorebook commands"""
    print("="*60)
    print("  LOREBOOK COMMAND SIMULATION")
    print("="*60)
    print("\nThis shows what each command does (simulated):\n")
    
    # Setup
    config_path = "simulate_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    # Command 1: Create lorebook
    print_command("!lorebook create fantasy_world")
    config_mgr.add_lorebook("fantasy_world", active=True)
    print("✓ Lorebook 'fantasy_world' created and activated.")
    
    # Command 2: List lorebooks
    print_command("!lorebook list")
    lorebooks = config_mgr.get_lorebooks()
    print("**Lorebooks:**")
    for i, lb in enumerate(lorebooks):
        status = "✓ Active" if lb.get("active") else "✗ Inactive"
        entry_count = len(lb.get("entries", []))
        print(f"{i+1}. **{lb.get('name')}** - {status} ({entry_count} entries)")
    
    # Command 3: Add constant entry
    print_command('!lorebook addentry fantasy_world constant "This is a high-fantasy world with magic."')
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "This is a high-fantasy world with magic.",
        insertion_type="constant"
    )
    print("✓ Constant entry added to lorebook 'fantasy_world'.")
    
    # Command 4: Add normal entry with keywords
    print_command('!lorebook addentry fantasy_world normal "Dragons are wise, ancient beings." dragon dragons')
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "Dragons are wise, ancient beings.",
        insertion_type="normal",
        keywords=["dragon", "dragons"]
    )
    print("✓ Normal entry added to lorebook 'fantasy_world' with keywords: dragon, dragons.")
    
    # Command 5: Add another normal entry
    print_command('!lorebook addentry fantasy_world normal "Elves live in magical forests." elf elves')
    config_mgr.add_lorebook_entry(
        "fantasy_world",
        "Elves live in magical forests.",
        insertion_type="normal",
        keywords=["elf", "elves"]
    )
    print("✓ Normal entry added to lorebook 'fantasy_world' with keywords: elf, elves.")
    
    # Command 6: Show lorebook
    print_command("!lorebook show fantasy_world")
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    entries = lorebook.get("entries", [])
    status = "Active" if lorebook.get("active") else "Inactive"
    print(f"**Lorebook: fantasy_world** ({status})")
    print()
    for i, entry in enumerate(entries):
        entry_type = entry.get("insertion_type", "normal").upper()
        content = entry.get("content", "")
        keywords = entry.get("keywords", [])
        print(f"**Entry {i}** [{entry_type}]")
        print(f"  Content: {content}")
        if keywords:
            print(f"  Keywords: {', '.join(keywords)}")
        print()
    
    # Command 7: Demonstrate keyword matching
    print("\n" + "="*60)
    print("  TESTING KEYWORD MATCHING")
    print("="*60)
    
    test_messages = [
        "What is this place?",
        "Tell me about dragons",
        "Are there elves here?",
        "Do dragons and elves get along?"
    ]
    
    for msg in test_messages:
        print(f"\nUser message: \"{msg}\"")
        entries = config_mgr.get_active_lorebook_entries(msg)
        print(f"Entries sent to AI: {len(entries)}")
        for i, entry in enumerate(entries):
            snippet = entry[:50] + "..." if len(entry) > 50 else entry
            print(f"  {i+1}. {snippet}")
    
    # Command 8: Deactivate lorebook
    print("\n" + "="*60)
    print_command("!lorebook deactivate fantasy_world")
    config_mgr.toggle_lorebook_active("fantasy_world", False)
    print("✓ Lorebook 'fantasy_world' deactivated.")
    
    # Show effect
    print_command('!chat Tell me about dragons (with lorebook deactivated)')
    entries = config_mgr.get_active_lorebook_entries("Tell me about dragons")
    print(f"Entries sent to AI: {len(entries)} (none, because lorebook is inactive)")
    
    # Command 9: Reactivate
    print_command("!lorebook activate fantasy_world")
    config_mgr.toggle_lorebook_active("fantasy_world", True)
    print("✓ Lorebook 'fantasy_world' activated.")
    
    # Command 10: Delete entry
    print_command("!lorebook delentry fantasy_world 1")
    config_mgr.delete_lorebook_entry("fantasy_world", 1)
    print("✓ Entry 1 deleted from lorebook 'fantasy_world'.")
    
    # Show updated lorebook
    print_command("!lorebook show fantasy_world")
    lorebook = config_mgr.get_lorebook_by_name("fantasy_world")
    entries = lorebook.get("entries", [])
    print(f"**Lorebook: fantasy_world** (Active)")
    print(f"\nNow has {len(entries)} entries (deleted the dragon entry)")
    for i, entry in enumerate(entries):
        entry_type = entry.get("insertion_type", "normal").upper()
        content = entry.get("content", "")[:50]
        print(f"  Entry {i} [{entry_type}]: {content}")
    
    # Command 11: List again
    print_command("!lorebook list")
    lorebooks = config_mgr.get_lorebooks()
    print("**Lorebooks:**")
    for i, lb in enumerate(lorebooks):
        status = "✓ Active" if lb.get("active") else "✗ Inactive"
        entry_count = len(lb.get("entries", []))
        print(f"{i+1}. **{lb.get('name')}** - {status} ({entry_count} entries)")
    
    # Command 12: Delete lorebook
    print_command("!lorebook delete fantasy_world")
    index = config_mgr.get_lorebook_index_by_name("fantasy_world")
    config_mgr.delete_lorebook(index)
    print("✓ Lorebook 'fantasy_world' deleted.")
    
    # Final check
    print_command("!lorebook list")
    lorebooks = config_mgr.get_lorebooks()
    if not lorebooks:
        print("No lorebooks found. Use `!lorebook create <name>` to create one.")
    
    # Cleanup
    os.remove(config_path)
    
    print("\n" + "="*60)
    print("  SIMULATION COMPLETE")
    print("="*60)
    print("\nAll commands demonstrated successfully!")
    print("\nThis is how the lorebook commands work in Discord.")
    print("Try them out with: python start.py")
    print()


if __name__ == "__main__":
    simulate_commands()
