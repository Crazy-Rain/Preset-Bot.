# Quick Reference Guide

## New Features Quick Reference

### 1. Adding a Character with Scenario

**GUI:**
```
Characters Tab → Fill Form
├── Character Name: storyteller
├── Display Name: Story Teller  
├── Description: You are a creative storyteller
├── Scenario: You are in a fantasy tavern ← NEW FIELD
└── Avatar: (optional URL or file)
→ Click "Add Character"
```

### 2. Editing an Existing Character

**GUI:**
```
Characters Tab
├── Select character from list
├── Click "Edit Selected" ← NEW BUTTON
├── Modify any fields (including scenario)
└── Click "Update Selected" ← NEW BUTTON
   (or "Clear Form" to cancel)
```

**Same workflow for User Characters tab**

### 3. Updating Character Avatar via Bot Command

**Discord:**
```
Method 1: Using URL
!image dashie https://i.imgur.com/avatar.png

Method 2: Using Attachment
!image dashie
(attach image to the message)
```

**What happens:**
- Downloads the image
- Saves to `character_avatars/dashie.png`
- Updates character config with both URL and file path

### 4. Saving AI Configuration Options

**GUI:**
```
Presets Tab
├── Adjust AI Configuration Options
│   ├── Max Tokens
│   ├── Temperature
│   ├── Top P
│   ├── Reasoning settings
│   └── Penalty settings
→ Go to Configuration Tab
→ Click "Save Configuration" ← This now saves AI options too!
```

## Configuration File Structure

### Character with Scenario
```json
{
  "characters": [
    {
      "name": "storyteller",
      "display_name": "Story Teller",
      "description": "You are a creative storyteller",
      "scenario": "You are in a fantasy tavern",
      "avatar_url": "https://example.com/avatar.png",
      "avatar_file": "character_avatars/storyteller.png"
    }
  ]
}
```

### AI Configuration Options
```json
{
  "ai_config_options": {
    "max_tokens": 4096,
    "response_length": 1024,
    "temperature": 1.0,
    "top_p": 1.0,
    "reasoning_enabled": false,
    "reasoning_level": "Auto",
    "use_presence_penalty": false,
    "presence_penalty": 0.0,
    "use_frequency_penalty": false,
    "frequency_penalty": 0.0
  }
}
```

## Common Workflows

### Create a Character with Full Details
1. Open GUI
2. Go to Characters tab
3. Fill in all fields:
   - Name (ID): `fantasy_guide`
   - Display Name: `Fantasy Guide`
   - Description: `You are an expert in fantasy worlds`
   - Scenario: `You are in a mystical library full of ancient tomes`
   - Avatar URL: `https://example.com/guide.png` (or use Browse for local file)
4. Click "Add Character"

### Edit a Character
1. Go to Characters tab
2. Select character from list
3. Click "Edit Selected"
4. Make changes
5. Click "Update Selected"

### Update Character Avatar from Discord
1. Find a nice avatar image online
2. In Discord channel where bot is active:
   ```
   !image fantasy_guide https://example.com/new-avatar.png
   ```
3. Bot downloads and updates the avatar

### Configure AI Settings
1. Open GUI
2. Go to Presets tab
3. Adjust settings (temperature, max tokens, etc.)
4. Go to Configuration tab
5. Click "Save Configuration"
6. Settings are now saved and will persist

## Troubleshooting

### Scenario field not showing?
- Scenario is ONLY for Characters, not User Characters
- Make sure you're on the "Characters" tab, not "User Characters"

### Edit button not working?
- Make sure you've selected a character from the list first
- The character will be highlighted when selected

### !image command fails?
- Ensure character name is spelled correctly
- Character must already exist
- URL must be publicly accessible
- Supported formats: PNG, JPG, JPEG, GIF, WEBP

### AI options not saving?
- Make sure to click "Save Configuration" in the Configuration tab
- The Presets tab only displays the options
- Saving happens in the Configuration tab

## Testing

Run tests to verify everything works:
```bash
python3 test_character_features.py
python3 test_new_features.py
```

Expected output: All tests should PASS ✅

## File Locations

- **Config file**: `config.json`
- **Character avatars**: `character_avatars/`
- **Documentation**: 
  - `NEW_FEATURES.md` - Full feature documentation
  - `GUI_CHANGES.md` - Visual guide
  - `IMPLEMENTATION_CHECKLIST.md` - Implementation details
  - `QUICK_REFERENCE.md` - This file
