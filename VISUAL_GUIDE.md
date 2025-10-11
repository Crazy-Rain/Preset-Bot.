# Visual Guide - Preset Bot GUI

## Overview
This guide shows the new GUI tabs and features added to Preset Bot.

## GUI Tabs

The GUI now has **5 tabs** (previously 3):

1. Configuration
2. **Presets** (NEW!)
3. Manual Send
4. Characters
5. **User Characters** (NEW!)

---

## Tab 1: Configuration

Standard configuration tab for:
- Discord bot token
- OpenAI API base URL
- OpenAI API key

*Screenshot saved as: gui_config_tab.png*

---

## Tab 2: Presets (NEW!)

### Features:

**AI Configuration Options Section:**
- Max Tokens / Context Length (up to 2,000,000)
- Response Length (Max Tokens)
- Temperature (0.0 - 2.0)
- Top P (0.0 - 1.0)
- Model Reasoning (checkbox + level dropdown)
- Presence Penalty (toggleable + value)
- Frequency Penalty (toggleable + value)

**Preset Message Blocks Section:**
- Add multiple blocks
- Each block has:
  - Active/Inactive checkbox
  - Role dropdown (system/user/assistant)
  - Content text area
  - Delete button

**Preset Management Section:**
- Preset name input
- Save Preset button
- Load Preset button
- Set as Active button
- Saved Presets dropdown

*Screenshots:*
- Empty presets tab: gui_presets_tab.png
- With added block: gui_presets_with_block.png

### UI Layout

```
┌─────────────────────────────────────────────────────┐
│ [Configuration] [Presets*] [Manual Send] ...       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌─ AI Configuration Options ──────────────────┐   │
│ │ Max Tokens:        [4096        ]           │   │
│ │ Response Length:   [1024        ]           │   │
│ │ Temperature:       [1.0         ]           │   │
│ │ Top P:             [1.0         ]           │   │
│ │ Model Reasoning:   [✓] Enable               │   │
│ │ Reasoning Level:   [Auto        ▼]          │   │
│ │ [✓] Presence Penalty:  [0.0     ]           │   │
│ │ [✓] Frequency Penalty: [0.0     ]           │   │
│ └─────────────────────────────────────────────┘   │
│                                                     │
│ ┌─ Preset Message Blocks ─────────────────────┐   │
│ │ Add message blocks sent to AI:               │   │
│ │ [+ Add New Block]                            │   │
│ │                                              │   │
│ │ ┌─ Block 1 ────────────────────────────┐   │   │
│ │ │ [✓] Active  Role: [system    ▼]     │   │   │
│ │ │ Content:                              │   │   │
│ │ │ ┌─────────────────────────────────┐ │   │   │
│ │ │ │ You are a helpful assistant     │ │   │   │
│ │ │ └─────────────────────────────────┘ │   │   │
│ │ │              [Delete Block]          │   │   │
│ │ └──────────────────────────────────────┘   │   │
│ └──────────────────────────────────────────────┘   │
│                                                     │
│ ┌─ Preset Management ──────────────────────────┐   │
│ │ Preset Name: [my_preset             ]        │   │
│ │ [Save Preset] [Load Preset] [Set as Active] │   │
│ │ Saved Presets: [my_preset          ▼]       │   │
│ └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Tab 3: Manual Send

Unchanged - allows sending manual messages to Discord channels with AI responses.

---

## Tab 4: Characters

Existing AI character management tab.
- Add/manage AI characters (used by the bot to respond)
- Avatar support (URL or file upload)

*Screenshot: gui_characters_tab.png*

---

## Tab 5: User Characters (NEW!)

### Features:

Similar to Characters tab but for user/player profiles:

**Add New User Character Section:**
- Character Name (ID) - lowercase identifier
- Display Name - shown in chat
- Description - character background/personality
- Avatar/Icon:
  - Avatar URL input
  - OR Avatar File upload (browse button)
- Add User Character button

**Current User Characters Section:**
- List of all user characters
- Shows: Display Name (ID): Description preview
- Refresh List button
- Delete Selected button

*Screenshot: gui_user_characters_tab.png*

### UI Layout

```
┌─────────────────────────────────────────────────────┐
│ [Configuration] [Presets] [Manual] [Chars] [Users*]│
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌─ Add New User Character ────────────────────┐   │
│ │ Character Name (ID): [alice    ]            │   │
│ │                      (lowercase, no spaces)  │   │
│ │ Display Name:        [Alice    ]            │   │
│ │                      (shown in chat)         │   │
│ │ Description:                                 │   │
│ │ ┌───────────────────────────────────────┐  │   │
│ │ │ A brave adventurer who loves          │  │   │
│ │ │ exploring dungeons.                   │  │   │
│ │ └───────────────────────────────────────┘  │   │
│ │ ┌─ Avatar/Icon ──────────────────────┐    │   │
│ │ │ Avatar URL: [https://...         ] │    │   │
│ │ │          --- OR ---                 │    │   │
│ │ │ Avatar File: [          ] [Browse] │    │   │
│ │ └────────────────────────────────────┘    │   │
│ │             [Add User Character]           │   │
│ └────────────────────────────────────────────┘   │
│                                                     │
│ ┌─ Current User Characters ────────────────────┐   │
│ │ Alice (alice): A brave adventurer...        │   │
│ │ Bob (bob): A wise wizard who...             │   │
│ │                                              │   │
│ │ [Refresh List] [Delete Selected]            │   │
│ └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Usage Flow

### Creating and Using a Preset

1. **Open GUI**: `python gui.py`
2. **Go to Presets tab**
3. **Configure AI options**:
   - Set temperature, tokens, etc.
4. **Add message blocks**:
   - Click "+ Add New Block"
   - Set role (system/user/assistant)
   - Enter content
   - Repeat for multiple blocks
5. **Save preset**:
   - Enter preset name
   - Click "Save Preset"
6. **Activate preset**:
   - Select from dropdown
   - Click "Set as Active"

### Creating User Characters

1. **Go to User Characters tab**
2. **Fill in character info**:
   - Name ID (e.g., "alice")
   - Display name (e.g., "Alice")
   - Description
   - Avatar (optional)
3. **Click "Add User Character"**
4. **Character appears in list**

### Using Chat with Characters

In Discord:
```
!chat alice: "Hello there!" waves enthusiastically
```

The bot will:
- Recognize "alice" as a user character
- Include character context
- Track the conversation
- Respond using active preset and AI character

---

## Color Scheme

- **Input fields**: Standard white background
- **Labels**: Black text
- **Sections**: Gray borders (LabelFrame)
- **Buttons**: Standard button styling
- **Status messages**: Color-coded
  - Green: Success
  - Red: Error
  - Blue: In progress

---

## Keyboard Navigation

- Tab key moves between fields
- Enter in text fields doesn't submit (use buttons)
- Scrollable areas support mouse wheel

---

## Best Practices

### For Presets
- Name presets descriptively (e.g., "creative_writing", "technical_support")
- Start with few blocks, add complexity as needed
- Use Active/Inactive toggles to test variations
- Keep temperature between 0.7-1.2 for most uses

### For User Characters
- Use short, memorable IDs
- Add rich descriptions for better AI understanding
- Upload avatars for visual identification

### For Message Blocks
- Use system role for instructions
- Use user/assistant pairs to show examples
- Keep each block focused on one aspect
- Toggle inactive instead of deleting for testing

---

## Screenshots Available

1. `gui_config_tab.png` - Configuration tab
2. `gui_presets_tab.png` - Empty presets tab
3. `gui_presets_with_block.png` - Presets tab with block added
4. `gui_characters_tab.png` - AI Characters tab
5. `gui_user_characters_tab.png` - User Characters tab

---

## Technical Notes

- All settings persist to `config.json`
- GUI updates config in real-time when saving
- Refresh buttons reload from config file
- Delete operations remove from both memory and file
- Avatar files copied to `character_avatars/` directory

---

## Troubleshooting

**Issue**: Preset not applying
**Solution**: Click "Set as Active" after loading/saving

**Issue**: User character not found in chat
**Solution**: Check spelling - names are case-insensitive but must match

**Issue**: GUI not responding
**Solution**: Close and reopen - all changes are saved

**Issue**: Avatar not showing
**Solution**: Use direct image URLs (ending in .png, .jpg, etc.)

---

For detailed documentation, see:
- [PRESET_FEATURES.md](PRESET_FEATURES.md) - Complete feature documentation
- [QUICKSTART_PRESETS.md](QUICKSTART_PRESETS.md) - Quick start guide
- [README.md](README.md) - Main documentation
