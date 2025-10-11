# Enhanced Character Tab - GUI Mockup

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Preset Discord Bot - Configuration & Manual Send            [_][□][×]  │
├─────────────────────────────────────────────────────────────────────────┤
│  [Configuration] [Manual Send] [Characters]                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─ Add New Character ──────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  Character Name (ID):  [tech_support___________] (lowercase, no  │  │
│  │                                                   spaces)         │  │
│  │                                                                   │  │
│  │  Display Name:         [Tech Support___________] (shown in       │  │
│  │                                                   Discord)        │  │
│  │                                                                   │  │
│  │  Description:         ┌──────────────────────────────────────┐  │  │
│  │  (AI system prompt)   │You are a technical support           │  │  │
│  │                       │specialist. Provide clear, step-by-   │  │  │
│  │                       │step solutions to technical problems. │  │  │
│  │                       │Be patient and helpful.               │  │  │
│  │                       │↕                                     │  │  │
│  │                       └──────────────────────────────────────┘  │  │
│  │                                                                   │  │
│  │  ┌─ Avatar/Icon ────────────────────────────────────────────┐   │  │
│  │  │                                                           │   │  │
│  │  │  Avatar URL:  [https://example.com/avatar.png_______]   │   │  │
│  │  │                                                           │   │  │
│  │  │                    --- OR ---                            │   │  │
│  │  │                                                           │   │  │
│  │  │  Avatar File: [character_avatars/tech.png] [Browse...]  │   │  │
│  │  │                                                           │   │  │
│  │  └───────────────────────────────────────────────────────────┘   │  │
│  │                                                                   │  │
│  │                                      [Add Character]             │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌─ Current Characters ─────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │  Assistant (assistant): You are a helpful assistant.         ↕  │  │
│  │  Tech Support (tech_support): You are a technical support...    │  │
│  │  Creative Writer (story_teller): You are a creative stor...     │  │
│  │                                                                   │  │
│  │  [Refresh List]  [Delete Selected]                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Character Configuration Example

### After Adding a Character:

**Character Details:**
- **Name (ID)**: `tech_support`
- **Display Name**: `Tech Support`
- **Description**: `You are a technical support specialist. Provide clear, step-by-step solutions to technical problems. Be patient and helpful.`
- **Avatar**: `character_avatars/tech_support.png` (uploaded file)

### How Messages Appear in Discord:

When you use the "Manual Send" feature with this character:

```
┌─────────────────────────────────────────┐
│  #general                         🔍 📌 │
├─────────────────────────────────────────┤
│                                         │
│  👤 Tech Support          [Bot] 2:30 PM │
│  Here's how to fix your issue:         │
│  1. First, check your internet...      │
│  2. Then restart your router...        │
│  3. Finally, clear your cache...       │
│                                         │
└─────────────────────────────────────────┘
```

**Note**: The message appears with:
- ✅ Character's Display Name (`Tech Support`)
- ✅ Character's Avatar (the uploaded image)
- ✅ [Bot] tag (from webhook)
- ✅ NOT as the bot's original identity

## Webhook Benefits Visualization

### Before (Old Method):
```
Bot sends as itself → Must change bot name/avatar → Limited tokens
```

### After (Webhook Method):
```
Bot creates webhook → Sends as character → Unlimited character variety!
```

**Advantages:**
1. 🎭 Multiple personalities without bot identity changes
2. 📝 Better message organization and identification
3. 🚀 2000+ character limit per message
4. 👥 Multiple characters in same channel
5. 🎨 Each character has unique name and avatar

## File Organization

```
Preset-Bot./
├── character_avatars/
│   ├── .gitkeep
│   ├── tech_support.png       ← Uploaded avatars stored here
│   ├── story_teller.jpg
│   └── assistant.png
├── config.json
│   └── Contains all character definitions
├── bot.py                      ← Webhook logic
├── gui.py                      ← Enhanced character tab
└── CHARACTER_GUIDE.md          ← Full documentation
```

## Usage Flow

1. **Open GUI** → Navigate to Characters tab
2. **Fill Form**:
   - Name: `tech_support` (ID for commands)
   - Display Name: `Tech Support` (shown in Discord)
   - Description: System prompt for AI behavior
   - Avatar: Browse for image OR paste URL
3. **Click "Add Character"**
4. **Character is Ready!** Can now be used in Manual Send

## Features Summary

✅ **Name Field**: Internal ID (lowercase, underscores)
✅ **Display Name Field**: Pretty name for Discord
✅ **Description Field**: AI personality/behavior
✅ **Browse Function**: Select image from device
✅ **URL Option**: Alternative to file upload
✅ **Images Saved**: Stored in `character_avatars/`
✅ **Webhook Sending**: Messages appear as character
✅ **Higher Limits**: Webhook character/token limits
✅ **Delete Function**: Remove characters with cleanup
✅ **Backward Compatible**: Old configs still work
