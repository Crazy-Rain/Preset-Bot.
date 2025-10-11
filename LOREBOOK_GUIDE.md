# Lorebook Feature Documentation

## Overview

The Lorebook feature allows you to create contextual information repositories that automatically inject relevant information into AI conversations. Similar to SillyTavern's lorebook system, you can create multiple lorebooks with entries that are either always active or triggered by keywords.

## Lorebook Structure

### Lorebooks
- **Name**: Unique identifier for the lorebook
- **Active/Inactive**: Toggle whether this lorebook is currently in use
- **Entries**: List of information entries

### Entries
Each entry has:
- **Content**: The information to inject into the conversation
- **Insertion Type**: 
  - `constant`: Always sent to the AI when the lorebook is active
  - `normal`: Only sent when keywords match the user's message
- **Keywords**: List of trigger words (only for normal entries)

## Bot Commands

### Create a Lorebook
```
!lorebook create <name>
```
Creates a new lorebook with the specified name (automatically activated).

**Example:**
```
!lorebook create fantasy_world
✓ Lorebook 'fantasy_world' created and activated.
```

### List Lorebooks
```
!lorebook list
```
Shows all lorebooks with their status and entry counts.

**Example:**
```
!lorebook list

**Lorebooks:**
1. **fantasy_world** - ✓ Active (5 entries)
2. **sci_fi_world** - ✗ Inactive (3 entries)
```

### Activate/Deactivate a Lorebook
```
!lorebook activate <name>
!lorebook deactivate <name>
```
Toggle whether a lorebook is active.

**Example:**
```
!lorebook activate fantasy_world
✓ Lorebook 'fantasy_world' activated.

!lorebook deactivate sci_fi_world
✓ Lorebook 'sci_fi_world' deactivated.
```

### Show Lorebook Entries
```
!lorebook show <name>
```
Display all entries in a lorebook.

**Example:**
```
!lorebook show fantasy_world

**Lorebook: fantasy_world** (Active)

**Entry 0** [CONSTANT]
  Content: This is a high-fantasy medieval world with magic.

**Entry 1** [NORMAL]
  Content: Dragons are intelligent, magical creatures that speak telepathically.
  Keywords: dragon, dragons

**Entry 2** [NORMAL]
  Content: Magic users are called Mages and draw power from the elemental planes.
  Keywords: magic, mage, spell, spells
```

### Add Entry to Lorebook
```
!lorebook addentry <lorebook_name> <constant|normal> <content> [keywords...]
```

**For Constant Entries:**
```
!lorebook addentry fantasy_world constant "This world has three moons in the night sky."
✓ Constant entry added to lorebook 'fantasy_world'.
```

**For Normal Entries with Keywords:**
```
!lorebook addentry fantasy_world normal "Elves live for thousands of years in forest cities." elf elves forest
✓ Normal entry added to lorebook 'fantasy_world' with keywords: elf, elves, forest.
```

**Note**: Use quotes around multi-word content to keep it together as one argument.

### Delete Entry from Lorebook
```
!lorebook delentry <lorebook_name> <entry_index>
```
Delete an entry by its index (shown in `!lorebook show`).

**Example:**
```
!lorebook delentry fantasy_world 2
✓ Entry 2 deleted from lorebook 'fantasy_world'.
```

### Delete a Lorebook
```
!lorebook delete <name>
```
Completely remove a lorebook and all its entries.

**Example:**
```
!lorebook delete old_world
✓ Lorebook 'old_world' deleted.
```

## How It Works

### Entry Injection Process

1. **User sends a message**: `!chat Tell me about dragons in this land.`

2. **System checks active lorebooks**:
   - Looks for lorebooks with `active: true`
   - Collects all **constant** entries immediately
   - Checks message for keywords and collects matching **normal** entries

3. **Entries are injected into AI context**:
   ```
   [System Prompt: Character description]
   [Lorebook: Constant entries + Keyword-triggered entries]
   [Chat History: Previous conversation]
   [Current Message: User's question]
   ```

4. **AI generates response** with lorebook context

### Example Flow

**Setup:**
```
!lorebook create fantasy_world
!lorebook addentry fantasy_world constant "Magic is common in this realm."
!lorebook addentry fantasy_world normal "Dragons are wise and ancient." dragon dragons
!lorebook addentry fantasy_world normal "Elves are immortal forest dwellers." elf elves
```

**User message without keywords:**
```
!chat What kind of world is this?
```
- AI receives: Constant entry only
- Result: AI knows about magic being common

**User message with 'dragon' keyword:**
```
!chat Tell me about dragons.
```
- AI receives: Constant entry + Dragon entry
- Result: AI knows about magic AND dragon lore

**User message with 'elf' keyword:**
```
!chat Are there elves here?
```
- AI receives: Constant entry + Elf entry
- Result: AI knows about magic AND elf lore

**User message with multiple keywords:**
```
!chat Can elves ride dragons?
```
- AI receives: Constant entry + Dragon entry + Elf entry
- Result: AI has full context about both species

## Best Practices

### Organizing Lorebooks

1. **Theme-based lorebooks**: Create separate lorebooks for different themes
   - `world_info`: General world setting
   - `character_lore`: Important NPCs and their backgrounds
   - `magic_system`: How magic works
   - `locations`: Places in the world

2. **Use constant entries sparingly**: Only for critical, always-relevant information
   - World's basic premise
   - Core rules that never change

3. **Use normal entries for details**: Most lore should be keyword-triggered
   - Specific characters
   - Locations
   - Items
   - Creatures

### Keyword Selection

1. **Use multiple keyword variations**:
   ```
   Keywords: dragon, dragons, drake, drakes, wyrm
   ```

2. **Include common misspellings or abbreviations**:
   ```
   Keywords: magic, magick, mage, wizard, spell
   ```

3. **Use both singular and plural forms**:
   ```
   Keywords: elf, elves, dwarf, dwarves
   ```

### Content Writing

1. **Be concise**: AI has token limits
   ```
   Good: "Dragons are intelligent, magical beings that live for millennia."
   Too long: "Dragons are extremely intelligent creatures who possess vast magical abilities including fire breathing, telepathy, shape-shifting, and..."
   ```

2. **Write in third person**: Helps maintain narrative consistency
   ```
   Good: "The capital city is built on floating islands."
   Less ideal: "You see the capital built on islands."
   ```

3. **Avoid contradictions**: Review entries to ensure consistency

## Integration with Other Features

### Works with Characters
Lorebooks work alongside character descriptions:
```
!character Gandalf
!lorebook activate middle_earth
```
Both the Gandalf character info AND Middle-earth lorebook will be sent to AI.

### Works with Presets
Lorebook entries are added after preset blocks but before chat history.

### Works with Chat History
Lorebook provides context, chat history provides conversation flow:
```
Message order:
1. Preset blocks (if active)
2. Character system prompt
3. Lorebook entries (constant + keyword-triggered)
4. Chat history (last 20 messages)
5. Current user message
```

## Configuration File Structure

Lorebooks are stored in `config.json`:

```json
{
  "lorebooks": [
    {
      "name": "fantasy_world",
      "active": true,
      "entries": [
        {
          "content": "This is a magical realm.",
          "insertion_type": "constant",
          "keywords": []
        },
        {
          "content": "Dragons are wise creatures.",
          "insertion_type": "normal",
          "keywords": ["dragon", "dragons"]
        }
      ]
    },
    {
      "name": "sci_fi_world",
      "active": false,
      "entries": []
    }
  ]
}
```

## Troubleshooting

### Entries Not Appearing

1. **Check if lorebook is active**:
   ```
   !lorebook list
   ```
   Look for ✓ Active status

2. **Verify keywords match**:
   Keywords are case-insensitive but must be in the message:
   ```
   Keyword: "dragon"
   Matches: "Dragon", "DRAGON", "Tell me about dragons"
   Doesn't match: "Tell me about reptiles"
   ```

3. **Check entry type**:
   - Normal entries only appear when keywords match
   - Constant entries always appear (if lorebook is active)

### Too Many Tokens

If you get token limit errors:

1. **Reduce constant entries**: Move some to normal entries with keywords
2. **Shorten entry content**: Be more concise
3. **Deactivate unused lorebooks**: Only keep relevant ones active
4. **Use fewer lorebooks**: Consolidate related entries

## Examples

### Fantasy RPG Setup

```bash
# Create world lorebook
!lorebook create fantasy_realm
!lorebook addentry fantasy_realm constant "This is a high-fantasy medieval world with magic and mythical creatures."
!lorebook addentry fantasy_realm normal "Dragons are ancient, wise beings who speak telepathically." dragon dragons drake
!lorebook addentry fantasy_realm normal "The Mage Guild controls all magical education and research." mage mages magic wizard
!lorebook addentry fantasy_realm normal "The capital city of Aetherhaven floats on enchanted clouds." aetherhaven capital city
!lorebook addentry fantasy_realm normal "Elves are immortal forest dwellers with natural magic." elf elves elven
```

### Sci-Fi Campaign Setup

```bash
# Create universe lorebook
!lorebook create space_opera
!lorebook addentry space_opera constant "Humanity has colonized the galaxy using FTL jump drives."
!lorebook addentry space_opera normal "The Galactic Council maintains peace between 50 alien species." council galactic
!lorebook addentry space_opera normal "Jump drives tear rifts in spacetime, enabling faster-than-light travel." jump ftl drive
!lorebook addentry space_opera normal "Earth was destroyed 200 years ago in the Great War." earth homeworld
```

### Mystery/Detective Setup

```bash
# Create case lorebook
!lorebook create noir_case
!lorebook addentry noir_case constant "This is 1940s New York City during the post-war era."
!lorebook addentry noir_case normal "Victor Mallory was a wealthy industrialist found dead in his penthouse." victor mallory victim
!lorebook addentry noir_case normal "Detective Sarah Chen is investigating the murder." sarah chen detective
!lorebook addentry noir_case normal "The Jade Dragon nightclub is a front for organized crime." jade dragon nightclub club
```

## Tips for DMs/Storytellers

1. **Prepare lorebooks before sessions**: Save time during gameplay

2. **Create character-specific lorebooks**: Different NPCs in different books
   ```
   !lorebook create npc_merchants
   !lorebook create npc_nobles
   !lorebook create npc_villains
   ```

3. **Toggle lorebooks for different areas**:
   ```
   # Players enter the city
   !lorebook deactivate wilderness
   !lorebook activate city_life
   ```

4. **Use for secrets and reveals**: Add entries when players discover them
   ```
   # After players learn about the hidden temple
   !lorebook addentry ancient_lore normal "The Temple of Secrets contains forbidden knowledge." temple secrets
   ```

5. **Track plot points**: Keep story consistent across sessions
   ```
   !lorebook addentry campaign_events constant "The dark prophecy was spoken three months ago during the blood moon."
   ```
