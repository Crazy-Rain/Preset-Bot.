"""
Demo: Lorebook Active/Inactive Visibility Improvements

This script demonstrates the enhanced visibility features for lorebook active/inactive states.
"""

import os
from bot import ConfigManager

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_section(text):
    """Print a formatted section"""
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70)

def demo_code_visibility():
    """Demonstrate code-side visibility improvements"""
    print_header("CODE-SIDE VISIBILITY DEMONSTRATION")
    
    config_path = "demo_visibility_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    print("\n📝 SETUP: Creating test lorebooks")
    # Create active lorebook
    config_mgr.add_lorebook("fantasy_world", active=True)
    config_mgr.add_lorebook_entry("fantasy_world", "This is a world of magic and wonder.", "constant")
    config_mgr.add_lorebook_entry("fantasy_world", "Dragons are majestic creatures.", "normal", ["dragon", "dragons"])
    print("   ✓ Created 'fantasy_world' (ACTIVE) with 2 entries")
    
    # Create inactive lorebook
    config_mgr.add_lorebook("scifi_world", active=False)
    config_mgr.add_lorebook_entry("scifi_world", "This is a futuristic sci-fi world.", "constant")
    config_mgr.add_lorebook_entry("scifi_world", "Robots are common in this world.", "normal", ["robot", "robots"])
    print("   ✓ Created 'scifi_world' (INACTIVE) with 2 entries")
    
    # Create another active lorebook
    config_mgr.add_lorebook("modern_world", active=True)
    config_mgr.add_lorebook_entry("modern_world", "This is a modern-day setting.", "constant")
    print("   ✓ Created 'modern_world' (ACTIVE) with 1 entry")
    
    print_section("SCENARIO 1: Processing message with mixed active/inactive lorebooks")
    print("\n📨 User message: 'Tell me about dragons'")
    print("\n🔍 Console output shows lorebook processing:")
    print("   (Notice how INACTIVE lorebooks are clearly marked as skipped)\n")
    
    message = "Tell me about dragons"
    entries = config_mgr.get_active_lorebook_entries(message)
    
    print(f"\n✅ RESULT: Retrieved {len(entries)} entries")
    print("   Expected: 3 entries (1 constant from fantasy_world, 1 dragon keyword from fantasy_world, 1 constant from modern_world)")
    print("   Inactive 'scifi_world' was skipped entirely")
    
    print_section("SCENARIO 2: Deactivating a lorebook")
    print("\n🖱️  Deactivating 'fantasy_world' lorebook...")
    config_mgr.toggle_lorebook_active("fantasy_world", False)
    print("   ✓ Deactivated")
    
    print("\n📨 User message: 'Tell me about dragons' (same as before)")
    print("\n🔍 Console output shows updated processing:\n")
    
    entries = config_mgr.get_active_lorebook_entries(message)
    
    print(f"\n✅ RESULT: Retrieved {len(entries)} entry/entries")
    print("   Expected: 1 entry (only from modern_world)")
    print("   Both 'fantasy_world' and 'scifi_world' were skipped (now both INACTIVE)")
    
    print_section("SCENARIO 3: Activating a lorebook")
    print("\n🖱️  Activating 'scifi_world' lorebook...")
    config_mgr.toggle_lorebook_active("scifi_world", True)
    print("   ✓ Activated")
    
    print("\n📨 User message: 'Tell me about robots'")
    print("\n🔍 Console output shows updated processing:\n")
    
    message = "Tell me about robots"
    entries = config_mgr.get_active_lorebook_entries(message)
    
    print(f"\n✅ RESULT: Retrieved {len(entries)} entries")
    print("   Expected: 3 entries (1 constant from scifi_world, 1 robot keyword from scifi_world, 1 constant from modern_world)")
    print("   'fantasy_world' remains INACTIVE and is skipped")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo cleanup complete")

def demo_gui_visibility():
    """Demonstrate GUI-side visibility improvements"""
    print_header("GUI-SIDE VISIBILITY DEMONSTRATION")
    
    print("\n📋 GUI ENHANCEMENTS:\n")
    
    print("1. LOREBOOK LIST - Enhanced Display")
    print("   Before: ✓ fantasy_world (2 entries)")
    print("   After:  ✓ ACTIVE | fantasy_world (2 entries)  [shown in GREEN]")
    print("   Before: ✗ scifi_world (2 entries)")
    print("   After:  ✗ INACTIVE | scifi_world (2 entries)  [shown in GRAY]")
    print("\n   ➜ Active lorebooks now appear in GREEN color")
    print("   ➜ Inactive lorebooks now appear in GRAY color")
    print("   ➜ Status is explicitly shown: 'ACTIVE' or 'INACTIVE'")
    
    print("\n2. STATUS INDICATOR - New Visual Element")
    print("   When a lorebook is selected:")
    print("   - Active lorebook shows:")
    print("     ┌─────────────────────────┐")
    print("     │  STATUS: ACTIVE ✓       │  [Light green background]")
    print("     └─────────────────────────┘   [Dark green text]")
    print("\n   - Inactive lorebook shows:")
    print("     ┌─────────────────────────┐")
    print("     │  STATUS: INACTIVE ✗     │  [Light red background]")
    print("     └─────────────────────────┘   [Dark red text]")
    
    print("\n3. BENEFITS")
    print("   ✅ At-a-glance visibility of active/inactive state")
    print("   ✅ Color coding makes status immediately obvious")
    print("   ✅ Explicit text labels remove any ambiguity")
    print("   ✅ Prominent status indicator for selected lorebook")
    print("   ✅ No need to activate/deactivate to check status")

def demo_complete_workflow():
    """Demonstrate a complete workflow showing visibility improvements"""
    print_header("COMPLETE WORKFLOW DEMONSTRATION")
    
    config_path = "demo_workflow_config.json"
    if os.path.exists(config_path):
        os.remove(config_path)
    
    config_mgr = ConfigManager(config_path)
    
    print("\n🎯 SCENARIO: User wants to test their lorebook changes")
    
    print_section("Step 1: Initial Setup")
    config_mgr.add_lorebook("character_lore", active=True)
    config_mgr.add_lorebook_entry("character_lore", "The hero is brave and noble.", "constant")
    print("✓ Created 'character_lore' lorebook (ACTIVE)")
    
    print_section("Step 2: Testing Initial State")
    print("📨 Sending test message...")
    print("🔍 Console shows:\n")
    entries = config_mgr.get_active_lorebook_entries("test")
    print(f"\n✅ {len(entries)} entry retrieved - lorebook is working!")
    
    print_section("Step 3: User Deactivates in GUI")
    print("🖱️  User clicks 'Deactivate' button")
    print("💾 Config saved")
    config_mgr.toggle_lorebook_active("character_lore", False)
    print("📺 GUI immediately updates:")
    print("   - List shows: ✗ INACTIVE | character_lore (1 entries) [in GRAY]")
    print("   - Status shows: STATUS: INACTIVE ✗ [red background]")
    
    print_section("Step 4: Testing Deactivated State")
    print("📨 Sending same test message...")
    print("🔍 Console shows:\n")
    entries = config_mgr.get_active_lorebook_entries("test")
    print(f"\n✅ {len(entries)} entries retrieved - lorebook is skipped!")
    print("✅ User can CLEARLY SEE that lorebook is inactive")
    
    print_section("Step 5: User Reactivates in GUI")
    print("🖱️  User clicks 'Activate' button")
    config_mgr.toggle_lorebook_active("character_lore", True)
    print("📺 GUI immediately updates:")
    print("   - List shows: ✓ ACTIVE | character_lore (1 entries) [in GREEN]")
    print("   - Status shows: STATUS: ACTIVE ✓ [green background]")
    
    print_section("Step 6: Testing Reactivated State")
    print("📨 Sending same test message...")
    print("🔍 Console shows:\n")
    entries = config_mgr.get_active_lorebook_entries("test")
    print(f"\n✅ {len(entries)} entry retrieved - lorebook is working again!")
    
    print("\n🎉 WORKFLOW COMPLETE")
    print("\n📊 VISIBILITY IMPROVEMENTS DEMONSTRATED:")
    print("   ✅ Console logging shows exactly which lorebooks are processed/skipped")
    print("   ✅ GUI color coding makes active/inactive immediately visible")
    print("   ✅ GUI status indicator provides prominent confirmation")
    print("   ✅ No ambiguity about whether activate/deactivate is working")
    
    # Cleanup
    os.remove(config_path)
    print("\n✓ Demo cleanup complete")

if __name__ == "__main__":
    print("=" * 70)
    print("  LOREBOOK VISIBILITY IMPROVEMENTS - COMPREHENSIVE DEMO")
    print("=" * 70)
    print("\nThis demo shows the enhanced visibility for lorebook active/inactive states")
    print("on both the CODE side (console logging) and GUI side (visual indicators).")
    
    demo_code_visibility()
    print("\n" + "=" * 70)
    demo_gui_visibility()
    print("\n" + "=" * 70)
    demo_complete_workflow()
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\n📌 KEY TAKEAWAYS:")
    print("   1. Console logs show EXACTLY which lorebooks are active/inactive")
    print("   2. GUI uses COLOR CODING (green=active, gray=inactive)")
    print("   3. GUI shows EXPLICIT STATUS labels (ACTIVE/INACTIVE)")
    print("   4. GUI has PROMINENT status indicator for selected lorebook")
    print("   5. No guesswork - visibility is clear at all times!")
    print()
