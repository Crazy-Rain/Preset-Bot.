# New Features Documentation

## Changes Summary

This update adds several new features to the Preset Bot:

### 1. Scenario Field for Characters

Characters (not User Characters) now have a new "Scenario" field that allows you to define a default situation or context for the character.

**GUI Usage:**
- Go to the "Characters" tab
- When adding or editing a character, you'll see a new "Scenario" text field
- Enter a scenario like: "You are in a fantasy tavern, ready to tell epic stories to adventurers"
- This scenario will be used as context when the character is active

**Config File:**
```json
{
  "characters": [
    {
      "name": "storyteller",
      "display_name": "Story Teller",
      "description": "You are a creative storyteller who crafts engaging narratives.",
      "scenario": "You are in a fantasy tavern, ready to tell stories to adventurers.",
      "avatar_url": "",
      "avatar_file": ""
    }
  ]
}
```

### 2. Edit Functionality for Characters

You can now edit existing characters without having to delete and recreate them.

**GUI Usage:**
1. Go to the "Characters" tab
2. Select a character from the list
3. Click "Edit Selected"
4. The character's data will load into the form
5. Modify any fields you want to change
6. Click "Update Selected" to save changes
7. Click "Clear Form" to cancel editing

**Notes:**
- The form title changes to "Add/Edit Character" 
- When editing, you can update all fields including name, display name, description, scenario, and avatars
- The "Add Character" button creates a new character
- The "Update Selected" button updates the selected character

### 3. Edit Functionality for User Characters

User Characters now also have edit functionality, just like regular Characters.

**GUI Usage:**
1. Go to the "User Characters" tab
2. Select a user character from the list
3. Click "Edit Selected"
4. Modify the fields
5. Click "Update Selected" to save changes
6. Click "Clear Form" to cancel editing

### 4. !image Command

A new bot command allows you to update character avatars by providing a URL or attaching an image.

**Command Syntax:**
```
!image <character_name> <url>
```
or
```
!image <character_name> (with image attached to the message)
```

**Examples:**
```
!image dashie https://i.imgur.com/example.png
```
Or attach an image to your Discord message and type:
```
!image dashie
```

**Features:**
- Downloads the image from the provided URL or attachment
- Saves the image to the `character_avatars/` directory
- Updates the character's avatar_url and avatar_file fields in the config
- Supports common image formats: PNG, JPG, JPEG, GIF, WEBP
- Provides feedback on success or failure

**Notes:**
- The character must already exist before you can update its avatar
- The image will be saved with the character's name as the filename
- Both the URL and local file path are stored for future use

### 5. AI Configuration Options Auto-Save

AI Configuration Options (in the Presets tab) are now automatically saved when you click "Save Configuration" in the Configuration tab.

**Settings that are now saved:**
- Max Tokens / Context Length
- Response Length (Max Tokens)
- Temperature
- Top P
- Model Reasoning (enabled/disabled)
- Reasoning Level (Auto, Maximum, High, Medium, Low, Minimum)
- Use Presence Penalty (enabled/disabled)
- Presence Penalty value
- Use Frequency Penalty (enabled/disabled)
- Frequency Penalty value

**How to use:**
1. Go to the "Presets" tab
2. Adjust the AI Configuration Options as desired
3. Go to the "Configuration" tab
4. Click "Save Configuration"
5. Your AI configuration options will be saved to the config file

**Config File:**
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

## API Changes

### ConfigManager Methods

**New/Updated Methods:**

```python
# Characters
config_manager.add_character(
    name="example",
    display_name="Example",
    description="Description",
    avatar_url="",
    avatar_file="",
    scenario="Default scenario"  # NEW parameter
)

config_manager.update_character(
    index=0,
    name="example",
    display_name="Updated Example",
    description="Updated description",
    avatar_url="",
    avatar_file="",
    scenario="Updated scenario"  # NEW parameter
)

# User Characters
config_manager.update_user_character(  # NEW method
    index=0,
    name="alice",
    display_name="Alice",
    description="Updated description",
    avatar_url="",
    avatar_file=""
)

# AI Config Options
config_manager.get_ai_config_options()  # NEW method
config_manager.set_ai_config_options(options_dict)  # NEW method
```

## Migration Notes

### Backward Compatibility

All changes are backward compatible:
- Existing characters without a "scenario" field will work normally (scenario defaults to empty string)
- Existing config files will load correctly
- Old format characters with "system_prompt" instead of "description" still work

### Updating Existing Characters

If you have existing characters and want to add scenarios:
1. Use the GUI's "Edit Selected" feature, or
2. Manually edit your config.json file to add the "scenario" field

## Requirements

A new dependency has been added:
```
aiohttp>=3.8.0
```

This is required for the !image command to download images from URLs.

To install:
```bash
pip install -r requirements.txt
```

## Testing

Run the test suite to verify all features work:
```bash
python3 test_character_features.py
python3 test_new_features.py
```

All tests should pass.
