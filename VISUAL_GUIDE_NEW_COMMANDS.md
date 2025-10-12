# Visual Guide: New Commands in Action

This guide shows what the new commands look like when used in Discord.

## !viewu - View User Character

### Command: `!viewu`
**When:** User wants to see which character they're currently using

**Input:**
```
!viewu
```

**Output (Discord Embed):**
```
┌─────────────────────────────────────────┐
│ User Character: Alice the Brave         │ [Green color]
├─────────────────────────────────────────┤
│ Character ID: alice                     │
│                                         │
│ [Thumbnail: Avatar image if available]  │
│                                         │
│ ┌─────────────────────────────┐        │
│ │  [Show Description] 🔵       │        │
│ └─────────────────────────────┘        │
└─────────────────────────────────────────┘
```

**When Button Clicked (Ephemeral - only you see it):**
```
┌─────────────────────────────────────────┐
│ Description                             │ [Blue color]
├─────────────────────────────────────────┤
│ A brave knight seeking justice and      │
│ defending the innocent. Armed with a    │
│ legendary sword and unwavering courage. │
└─────────────────────────────────────────┘
```

### Command: `!viewu alice`
**When:** User wants to see a specific user character's info

**Input:**
```
!viewu alice
```

**Output:**
Same as above, but shows the specified character instead of your active one.

---

## !viewc - View Channel Character

### Command: `!viewc`
**When:** User wants to see which AI character is responding in this channel

**Input:**
```
!viewc
```

**Output (Discord Embed):**
```
┌─────────────────────────────────────────┐
│ AI Character: The Dungeon Master        │ [Blue color]
├─────────────────────────────────────────┤
│ Character ID: dungeon_master            │
│                                         │
│ [Thumbnail: Avatar image if available]  │
│                                         │
│ ┌─────────────────────────────┐        │
│ │  [Show Description] 🔵       │        │
│ │  [Show Scenario] ⚪          │        │
│ └─────────────────────────────┘        │
└─────────────────────────────────────────┘
```

**When Show Description Button Clicked:**
```
┌─────────────────────────────────────────┐
│ Description                             │ [Blue color]
├─────────────────────────────────────────┤
│ A mysterious narrator who guides        │
│ players through epic adventures in a    │
│ fantasy realm. You describe scenes,     │
│ control NPCs, and respond to player     │
│ actions with dramatic flair.            │
└─────────────────────────────────────────┘
```

**When Show Scenario Button Clicked:**
```
┌─────────────────────────────────────────┐
│ Scenario                                │ [Blue color]
├─────────────────────────────────────────┤
│ You are narrating a fantasy D&D         │
│ campaign. The party is exploring an     │
│ ancient dungeon filled with traps and   │
│ treasures.                              │
└─────────────────────────────────────────┘
```

---

## !cimage - Update User Character Avatar

### Command: `!cimage alice https://example.com/alice.png`
**When:** User wants to add/update an avatar for a user character

**Input:**
```
!cimage alice https://example.com/alice.png
```

**Output (Text Messages):**
```
Downloading image for 'alice'...
✓ Avatar updated for user character 'Alice the Brave'!
```

### Command: `!cimage alice` (with attachment)
**When:** User wants to upload an image directly from their computer

**Input:**
```
!cimage alice
[Image file attached to message]
```

**Output:**
```
Downloading image for 'alice'...
✓ Avatar updated for user character 'Alice the Brave'!
```

---

## Complete Usage Scenario

### Setting Up a Character

**Step 1: Create character via GUI**
```
GUI > User Characters tab > Add New Character
Name: alice
Display Name: Alice the Brave
Description: A brave knight...
```

**Step 2: Add avatar**
```
Discord: !cimage alice https://example.com/alice.png
Bot: ✓ Avatar updated for user character 'Alice the Brave'!
```

**Step 3: Use in chat**
```
Discord: !chat alice: "I shall defend the innocent!"
Bot: [Response from AI character via webhook]
```

**Step 4: Verify setup**
```
Discord: !viewu
Bot: [Shows embed with Alice the Brave and avatar]
```

---

## Multi-User Scenario

### User 1 (Player 1)
```
Player1: !chat thorin: "I ready my warhammer!"
Bot: [DM responds via webhook as The Dungeon Master]

Player1: !viewu
Bot: 
┌─────────────────────────────────────────┐
│ User Character: Thorin Ironhammer       │
│ Character ID: thorin                    │
│ [Avatar thumbnail]                      │
│ [Show Description button]               │
└─────────────────────────────────────────┘
```

### User 2 (Player 2) - Same Channel
```
Player2: !chat elara: "I cast Light!"
Bot: [DM responds via webhook as The Dungeon Master]

Player2: !viewu
Bot: 
┌─────────────────────────────────────────┐
│ User Character: Elara Moonwhisper       │
│ Character ID: elara                     │
│ [Avatar thumbnail]                      │
│ [Show Description button]               │
└─────────────────────────────────────────┘
```

### Anyone Checks Channel Character
```
Anyone: !viewc
Bot: 
┌─────────────────────────────────────────┐
│ AI Character: The Dungeon Master        │
│ Character ID: dungeon_master            │
│ [Avatar thumbnail]                      │
│ [Show Description button]               │
│ [Show Scenario button]                  │
└─────────────────────────────────────────┘
```

---

## Error Messages

### No Active Character
```
User: !viewu
Bot: You haven't used a user character in !chat yet in this channel.
```

### Character Not Found
```
User: !viewu unknown_character
Bot: Error: User character 'unknown_character' not found.
```

### Missing URL/Attachment
```
User: !cimage alice
Bot: Error: Please provide either a URL or attach an image to the message.
```

### Download Failed
```
User: !cimage alice https://invalid.url/image.png
Bot: Error: Failed to download image (HTTP 404).
```

---

## Color Coding

- **Green Embeds** = User Characters (!viewu)
- **Blue Embeds** = AI Characters (!viewc)
- **Blue Buttons** = Interactive "Show Description" buttons
- **Ephemeral Responses** = Only the button clicker sees the description

---

## Button Interaction Flow

```
1. User runs !viewu or !viewc
   └─> Bot sends embed with button

2. User clicks [Show Description]
   └─> Discord sends interaction to bot

3. Bot responds with ephemeral message
   └─> Only the clicker sees the description

4. Button expires after 5 minutes
   └─> Run command again for a fresh button
```

---

## Tips for Best Experience

✅ **Do:**
- Set avatars before using characters (looks better!)
- Click the button to see full descriptions
- Use !viewu to confirm your active character

❌ **Don't:**
- Forget that buttons expire (5 min timeout)
- Mix up !viewu (user) with !viewc (AI)
- Try to view characters that don't exist

---

## Integration with Existing Commands

### Works With:
- `!chat` - Your !viewu character is what you use here
- `!character` - Sets what !viewc will show for the channel
- `!image` - Similar to !cimage but for AI characters
- `!clearchat` - Clears history (affects !viewu lookup)

### Related Commands:
```
!chat alice: "message"  →  Sets your active character
!viewu                   →  Shows that you're using alice
!character dm           →  Sets channel's AI character
!viewc                   →  Shows that channel uses dm
!cimage alice url       →  Updates alice's avatar
!image dm url           →  Updates dm's avatar
```

---

## Real-World Example: D&D Session

```
[Setup Phase]
GM: !character dungeon_master
GM: !viewc
Bot: [Shows The Dungeon Master with scenario]

Player1: !cimage thorin https://i.imgur.com/thorin.png
Bot: ✓ Avatar updated for user character 'Thorin Ironhammer'!

Player2: !cimage elara https://i.imgur.com/elara.png
Bot: ✓ Avatar updated for user character 'Elara Moonwhisper'!

[Game Time]
Player1: !chat thorin: "I approach the dungeon entrance carefully."
Bot (as DM): [Response about what Thorin sees]

Player1: !viewu
Bot: [Shows Thorin Ironhammer with avatar]

Player2: !chat elara: "I cast Detect Magic!"
Bot (as DM): [Response about magical auras]

Player2: !viewu
Bot: [Shows Elara Moonwhisper with avatar]

[Later - Player1 wants to remember their character]
Player1: !viewu
Player1: *clicks [Show Description]*
Bot: [Shows full description of Thorin - only Player1 sees it]
```

---

## Technical Notes

- **Embeds**: Use Discord's rich embed format
- **Colors**: RGB values for green/blue theme
- **Buttons**: Discord UI components (discord.ui.View/Button)
- **Ephemeral**: Button responses use `ephemeral=True`
- **Timeout**: Buttons auto-disable after 300 seconds (5 min)
- **Avatars**: Use `set_thumbnail()` for avatar display

---

This visual guide shows how the commands appear and behave in Discord. For implementation details, see IMPLEMENTATION_SUMMARY_NEW_COMMANDS.md.
