# Character System Guide

## Overview

The Preset Bot now features an enhanced character system that allows you to create AI personalities with custom names, descriptions, and avatars. Messages are sent via Discord webhooks, allowing each character to appear with their own name and avatar without modifying the bot's identity.

## Character Fields

Each character has the following fields:

### 1. Name (ID)
- **Format**: Lowercase, no spaces (e.g., `assistant`, `tech_expert`)
- **Purpose**: Internal identifier used in commands and code
- **Example**: `helpful_bot`

### 2. Display Name
- **Format**: Any text (e.g., `Helpful Bot`, `Tech Expert`)
- **Purpose**: Name shown in Discord when the character sends messages
- **Example**: `Helpful Bot`

### 3. Description
- **Format**: Free-form text
- **Purpose**: AI system prompt that defines the character's personality and behavior
- **Example**: `You are a helpful assistant who provides clear, concise answers.`

### 4. Avatar/Icon
You have two options for setting a character's avatar:

#### Option A: Avatar URL
- **Format**: Direct URL to an image
- **Purpose**: Use an image hosted online
- **Example**: `https://example.com/avatar.png`

#### Option B: Avatar File
- **Format**: Local image file (PNG, JPG, JPEG, GIF, WEBP)
- **Purpose**: Upload an image from your computer
- **Storage**: Files are copied to `character_avatars/` directory
- **Example**: Browse and select a file from your device

**Note**: Avatar URL takes precedence if both are provided.

## Creating Characters via GUI

1. **Open the GUI**
   ```bash
   python gui.py
   ```

2. **Navigate to the Characters tab**

3. **Fill in the character details:**
   - **Character Name (ID)**: Enter a unique identifier (e.g., `tech_support`)
   - **Display Name**: Enter the name to show in Discord (e.g., `Tech Support Bot`)
   - **Description**: Write the AI system prompt that defines behavior
   - **Avatar**: Either:
     - Enter a URL in the "Avatar URL" field, OR
     - Click "Browse..." to select an image file from your computer

4. **Click "Add Character"**

The character is now saved and ready to use!

## Creating Characters via Bot Command

```discord
!addcharacter <name> <display_name> <description>
```

**Example:**
```discord
!addcharacter tech_expert "Tech Expert" You are a technical expert who provides detailed, accurate solutions to technology problems.
```

**Note**: Bot commands cannot set avatars. Use the GUI or edit `config.json` directly to add avatars.

## Using Characters

### Manual Send (GUI)
1. Open the GUI and go to the "Manual Send" tab
2. Enter Server ID and Channel ID
3. Select a character from the dropdown
4. Type your message
5. Click "Send Message"

The bot will:
- Generate an AI response using the character's description
- Send the message via webhook with the character's display name and avatar

### Manual Send (Bot Command)
```discord
!manualsend <server_id> <channel_id> <character_name> <message>
```

**Example:**
```discord
!manualsend 123456789 987654321 tech_expert How do I fix a memory leak?
```

## Webhook Benefits

Characters send messages via Discord webhooks, which provides several advantages:

1. **Custom Identity**: Each character appears with their own name and avatar
2. **No Bot Modification**: The bot's identity remains unchanged
3. **Higher Message Limits**: Webhooks have a 2000 character limit (same as regular messages) but allow for better formatting
4. **Better Organization**: Users can easily distinguish between different AI characters

## Character Storage

### Configuration
Characters are stored in `config.json`:

```json
{
  "characters": [
    {
      "name": "tech_expert",
      "display_name": "Tech Expert",
      "description": "You are a technical expert...",
      "avatar_url": "https://example.com/avatar.png",
      "avatar_file": "character_avatars/tech_expert.png"
    }
  ]
}
```

### Avatar Files
- Uploaded avatar images are stored in `character_avatars/`
- File format: `<character_name>.<extension>`
- Example: `character_avatars/tech_expert.png`
- These files are git-ignored (not committed to version control)

## Managing Characters

### Listing Characters

**GUI**: Go to Characters tab, view "Current Characters" list

**Bot Command**:
```discord
!characters
```

### Deleting Characters

**GUI**: 
1. Go to Characters tab
2. Select a character in the list
3. Click "Delete Selected"
4. Confirm deletion

**Note**: Deleting a character also removes its avatar file if one exists.

### Editing Characters

To edit a character:
1. Delete the existing character
2. Create a new character with updated information

Or edit `config.json` directly and reload the bot.

## Advanced Configuration

### Editing config.json Directly

```json
{
  "characters": [
    {
      "name": "assistant",
      "display_name": "Assistant",
      "description": "You are a helpful assistant.",
      "avatar_url": "",
      "avatar_file": ""
    },
    {
      "name": "creative_writer",
      "display_name": "Creative Writer",
      "description": "You are a creative writer who crafts engaging stories.",
      "avatar_url": "https://example.com/writer.png",
      "avatar_file": ""
    }
  ]
}
```

### Migration from Old Format

If you have characters in the old format (with `system_prompt` field), they will still work. The bot automatically converts `system_prompt` to `description` internally for backward compatibility.

Old format:
```json
{
  "name": "Assistant",
  "system_prompt": "You are a helpful assistant."
}
```

New format (recommended):
```json
{
  "name": "assistant",
  "display_name": "Assistant",
  "description": "You are a helpful assistant.",
  "avatar_url": "",
  "avatar_file": ""
}
```

## Character Examples

### Tech Support Character
```json
{
  "name": "tech_support",
  "display_name": "Tech Support",
  "description": "You are a technical support specialist. Provide clear, step-by-step solutions to technical problems. Be patient and ask clarifying questions when needed.",
  "avatar_url": "https://example.com/tech-support-avatar.png",
  "avatar_file": ""
}
```

### Creative Writer Character
```json
{
  "name": "story_teller",
  "display_name": "Story Teller",
  "description": "You are a creative storyteller. Write engaging, imaginative stories with vivid descriptions and compelling characters. Use descriptive language and create emotional connections.",
  "avatar_url": "",
  "avatar_file": "character_avatars/story_teller.png"
}
```

### Educational Tutor Character
```json
{
  "name": "tutor",
  "display_name": "Math Tutor",
  "description": "You are an educational tutor specializing in mathematics. Explain concepts clearly with examples. Break down complex problems into simple steps. Encourage learning and understanding.",
  "avatar_url": "https://example.com/tutor-avatar.png",
  "avatar_file": ""
}
```

## Troubleshooting

### Character not showing in dropdown
- **Solution**: Click "Refresh List" in the GUI or restart the application

### Avatar not displaying
- **Possible causes**:
  - Invalid URL (check if URL is accessible)
  - File path incorrect (ensure file exists in `character_avatars/`)
  - Discord webhook limitations (avatar must be accessible via URL)
- **Solution**: Use a valid, publicly accessible image URL

### Webhook permission errors
- **Error**: "Missing Permissions" or "Forbidden"
- **Solution**: Ensure the bot has "Manage Webhooks" permission in the target channel

### Character name conflicts
- **Error**: Duplicate character names
- **Solution**: Each character must have a unique `name` (ID). Use different identifiers even if display names are similar.

## Best Practices

1. **Naming Convention**: Use lowercase with underscores for character names (IDs)
2. **Display Names**: Use readable, descriptive names for display names
3. **Descriptions**: Be specific about the character's role, tone, and expertise
4. **Avatars**: Use square images (1:1 aspect ratio) for best results
5. **Avatar Size**: Discord recommends 128x128 or larger for avatars
6. **Avatar URLs**: Ensure URLs are publicly accessible (not behind authentication)
7. **Testing**: Test new characters with simple messages before complex interactions

## API Reference

### ConfigManager Methods

```python
# Add a character
config_manager.add_character(
    name="tech_expert",
    display_name="Tech Expert",
    description="You are a technical expert...",
    avatar_url="https://example.com/avatar.png",
    avatar_file=""
)

# Get a character by name
character = config_manager.get_character_by_name("tech_expert")

# Update a character
config_manager.update_character(
    index=0,
    name="tech_expert",
    display_name="Tech Expert Pro",
    description="Updated description...",
    avatar_url="",
    avatar_file="character_avatars/expert.png"
)

# Delete a character
config_manager.delete_character(index=0)

# Get all characters
characters = config_manager.get_characters()
```

### Webhook Sending

```python
# Send via webhook (bot.py)
await bot.send_via_webhook(
    channel=channel,
    content="Message content",
    character={
        "name": "tech_expert",
        "display_name": "Tech Expert",
        "avatar_url": "https://example.com/avatar.png"
    }
)
```

## See Also

- [README.md](README.md) - Main documentation
- [FEATURES.md](FEATURES.md) - Feature overview
- [GUI_GUIDE.md](GUI_GUIDE.md) - GUI usage guide
- [config_template.json](config_template.json) - Configuration template
