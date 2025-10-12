#!/usr/bin/env python3
"""
Demo script to showcase the new commands
Simulates a realistic scenario with the new !viewu, !viewc, and !cimage commands
"""

import os
import sys
from bot import ConfigManager

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    """Demonstrate the new commands"""
    
    # Setup
    test_config_path = "demo_new_commands_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    print_section("Preset Bot - New Commands Demonstration")
    print("\nThis demo shows the three new commands:")
    print("  1. !viewu - View user character")
    print("  2. !viewc - View AI/Bot character")
    print("  3. !cimage - Update user character avatar")
    
    # Scenario 1: Setting up characters
    print_section("Step 1: Create Characters")
    
    print("\n📝 Creating AI character: 'dungeon_master'")
    config_mgr.add_character(
        name="dungeon_master",
        display_name="The Dungeon Master",
        description="A mysterious narrator who guides players through epic adventures in a fantasy realm.",
        avatar_url="https://example.com/dm.png",
        scenario="You are narrating a fantasy D&D campaign. The party is exploring an ancient dungeon."
    )
    print("   ✓ Created: The Dungeon Master")
    
    print("\n📝 Creating user characters:")
    config_mgr.add_user_character(
        name="thorin",
        display_name="Thorin Ironhammer",
        description="A brave dwarf warrior with a legendary warhammer. Courageous, loyal, and loves treasure.",
        avatar_url=""
    )
    print("   ✓ Created: Thorin Ironhammer (dwarf warrior)")
    
    config_mgr.add_user_character(
        name="elara",
        display_name="Elara Moonwhisper",
        description="An elven mage specializing in light magic. Wise, compassionate, and mysterious.",
        avatar_url=""
    )
    print("   ✓ Created: Elara Moonwhisper (elven mage)")
    
    # Scenario 2: Using !cimage to set avatars
    print_section("Step 2: Simulate !cimage Command")
    
    print("\n🖼️  Command: !cimage thorin https://example.com/thorin.png")
    config_mgr.update_user_character(
        index=0,
        name="thorin",
        display_name="Thorin Ironhammer",
        description="A brave dwarf warrior with a legendary warhammer. Courageous, loyal, and loves treasure.",
        avatar_url="https://example.com/thorin.png",
        avatar_file="character_avatars/thorin.png"
    )
    print("   ✓ Avatar updated for Thorin Ironhammer")
    
    print("\n🖼️  Command: !cimage elara https://example.com/elara.png")
    config_mgr.update_user_character(
        index=1,
        name="elara",
        display_name="Elara Moonwhisper",
        description="An elven mage specializing in light magic. Wise, compassionate, and mysterious.",
        avatar_url="https://example.com/elara.png",
        avatar_file="character_avatars/elara.png"
    )
    print("   ✓ Avatar updated for Elara Moonwhisper")
    
    # Scenario 3: Set channel character and simulate chat
    print_section("Step 3: Set Channel Character and Simulate Chat")
    
    channel_id = "channel_123"
    print(f"\n🎭 Command: !character dungeon_master")
    config_mgr.set_channel_character(channel_id, "dungeon_master")
    print("   ✓ Channel character set to 'The Dungeon Master'")
    
    print(f"\n💬 User1 uses: !chat thorin: \"I ready my warhammer!\"")
    config_mgr.add_chat_message(channel_id, {
        "author": "user_001",
        "author_name": "Player1",
        "user_character": "thorin",
        "content": "I ready my warhammer!",
        "type": "user",
        "timestamp": "2024-01-01T00:00:00"
    })
    print("   ✓ Message from Thorin Ironhammer recorded")
    
    print(f"\n💬 User2 uses: !chat elara: \"I cast Light!\"")
    config_mgr.add_chat_message(channel_id, {
        "author": "user_002",
        "author_name": "Player2",
        "user_character": "elara",
        "content": "I cast Light!",
        "type": "user",
        "timestamp": "2024-01-01T00:01:00"
    })
    print("   ✓ Message from Elara Moonwhisper recorded")
    
    # Scenario 4: Simulate !viewu command
    print_section("Step 4: Simulate !viewu Command")
    
    print("\n👤 User1 uses: !viewu")
    print("   Looking up User1's active character...")
    
    # Find User1's character
    chat_history = config_mgr.get_chat_history(channel_id)
    user1_char = None
    for msg in reversed(chat_history):
        if msg.get("author") == "user_001" and msg.get("user_character"):
            user1_char = msg.get("user_character")
            break
    
    if user1_char:
        char_data = config_mgr.get_user_character_by_name(user1_char)
        print(f"\n   📋 Response:")
        print(f"      Character: {char_data.get('display_name')}")
        print(f"      ID: {char_data.get('name')}")
        print(f"      Avatar: {char_data.get('avatar_url')}")
        print(f"      [Button: Show Description]")
        print(f"\n   ✓ User1's active character is Thorin Ironhammer")
    
    print("\n👤 User2 uses: !viewu")
    print("   Looking up User2's active character...")
    
    # Find User2's character
    user2_char = None
    for msg in reversed(chat_history):
        if msg.get("author") == "user_002" and msg.get("user_character"):
            user2_char = msg.get("user_character")
            break
    
    if user2_char:
        char_data = config_mgr.get_user_character_by_name(user2_char)
        print(f"\n   📋 Response:")
        print(f"      Character: {char_data.get('display_name')}")
        print(f"      ID: {char_data.get('name')}")
        print(f"      Avatar: {char_data.get('avatar_url')}")
        print(f"      [Button: Show Description]")
        print(f"\n   ✓ User2's active character is Elara Moonwhisper")
    
    # Scenario 5: Simulate !viewc command
    print_section("Step 5: Simulate !viewc Command")
    
    print("\n🤖 Anyone uses: !viewc")
    print("   Looking up channel's AI character...")
    
    ai_char_name = config_mgr.get_channel_character(channel_id)
    if ai_char_name:
        ai_char = config_mgr.get_character_by_name(ai_char_name)
        print(f"\n   📋 Response:")
        print(f"      Character: {ai_char.get('display_name')}")
        print(f"      ID: {ai_char.get('name')}")
        print(f"      Avatar: {ai_char.get('avatar_url')}")
        print(f"      Scenario: {ai_char.get('scenario')[:60]}...")
        print(f"      [Button: Show Description]")
        print(f"\n   ✓ Channel AI character is The Dungeon Master")
    
    # Scenario 6: View specific characters
    print_section("Step 6: View Specific Characters")
    
    print("\n🔍 Command: !viewu elara")
    elara = config_mgr.get_user_character_by_name("elara")
    print(f"   📋 Showing: {elara.get('display_name')}")
    print(f"      Description: {elara.get('description')[:60]}...")
    print(f"   ✓ Can view any user character by name")
    
    print("\n🔍 Command: !viewc dungeon_master")
    dm = config_mgr.get_character_by_name("dungeon_master")
    print(f"   📋 Showing: {dm.get('display_name')}")
    print(f"      Description: {dm.get('description')[:60]}...")
    print(f"   ✓ Can view any AI character by name")
    
    # Summary
    print_section("Summary")
    print("\n✅ Demonstrated all three new commands:")
    print("   • !cimage - Updated avatars for user characters")
    print("   • !viewu  - Viewed user characters (automatic and by name)")
    print("   • !viewc  - Viewed AI character (automatic and by name)")
    print("\n✅ Key features:")
    print("   • User characters tracked per Discord UserID")
    print("   • Each user has their own active character")
    print("   • Interactive buttons show full descriptions")
    print("   • Avatars displayed in embeds")
    print("   • Works with existing !chat and !character commands")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    print("\n" + "=" * 70)
    print("Demo complete! See NEW_COMMANDS_GUIDE.md for full documentation.")
    print("=" * 70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
