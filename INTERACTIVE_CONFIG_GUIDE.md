# Interactive Discord Configuration Guide

## Overview

The Interactive Discord Configuration system allows you to configure your bot directly from Discord without needing to stop the bot or access the GUI on the host machine. This feature uses Discord's interactive UI components (buttons and modals) to provide a user-friendly configuration experience.

## Key Benefits

1. **No Bot Restart Required**: Configure settings without stopping the Discord bot
2. **Remote Configuration**: No need to access the host machine's GUI
3. **User-Friendly Interface**: Interactive buttons and forms instead of command-line syntax
4. **Admin-Only Access**: Secure configuration with administrator permission checks
5. **Visual Feedback**: Clear embeds showing current configuration states

## Getting Started

### Opening the Configuration Menu

Simply use the `!config` command in any channel where the bot has permissions:

```text
!config
```

**Note**: You must have Administrator permissions to use this command.

### Configuration Menu

When you run `!config`, you'll see an interactive menu with the following buttons:

#### 🔧 OpenAI Config
Opens a modal form to configure OpenAI settings:
- **Base URL**: The API endpoint URL (e.g., `https://api.openai.com/v1`)
- **API Key**: Your OpenAI API key
- **Model**: The AI model to use (optional)

The form pre-fills with your current settings, making it easy to update specific values.

#### 🤖 Characters
Displays all configured AI characters with their:
- Display names
- Internal names
- Descriptions (truncated to 100 characters)

This is a view-only button that shows your current character configuration.

#### 👥 User Characters
Shows all user/player characters configured in the system with:
- Display names
- Internal names
- Descriptions (truncated to 100 characters)

Useful for seeing which user characters are available for role-playing.

#### ⚙️ Bot Settings
Displays current bot configuration including:
- **Reconnection Settings**:
  - Enabled/Disabled status
  - Maximum retry attempts
  - Base delay between retries
  - Maximum delay between retries

#### 📚 Lorebooks
Lists all configured lorebooks showing:
- Lorebook names
- Active/Inactive status
- Number of entries in each lorebook

#### 🎯 Presets
Shows all AI presets with:
- Preset names
- Active preset indicator (⭐)
- Number of message blocks in each preset

#### ❌ Close
Closes the configuration menu.

## Usage Examples

### Configuring OpenAI Settings

1. Type `!config` in Discord
2. Click the "🔧 OpenAI Config" button
3. Fill in the modal form:
   - Base URL: `https://api.openai.com/v1`
   - API Key: `sk-your-api-key-here`
   - Model: `gpt-4` (optional)
4. Click "Submit"
5. You'll receive a confirmation message with your settings (API key will be masked)

### Viewing Characters

1. Type `!config` in Discord
2. Click the "🤖 Characters" button
3. View the list of all configured AI characters
4. The message is only visible to you (ephemeral)

### Checking Bot Settings

1. Type `!config` in Discord
2. Click the "⚙️ Bot Settings" button
3. Review the current reconnection configuration
4. The settings are displayed in an easy-to-read embed

## Security Features

### Administrator-Only Access
The `!config` command requires Administrator permissions. Users without this permission will receive an error message.

### Ephemeral Messages
All configuration displays are ephemeral (only visible to you), preventing sensitive information from being seen by other users.

### API Key Masking
When displaying OpenAI configuration, the API key is masked with asterisks to prevent accidental exposure.

## Menu Timeout

The configuration menu automatically expires after **3 minutes** of inactivity. After this time, the buttons will no longer respond. Simply run `!config` again to open a new menu.

## Comparison with Other Configuration Methods

| Method | Requires Bot Restart | Remote Access | GUI Required | User-Friendly |
|--------|---------------------|---------------|--------------|---------------|
| Edit config.json | ❌ No | ✅ Yes | ❌ No | ⚠️ Moderate |
| GUI (gui.py) | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| Commands (!settoken, !setopenai) | ❌ No | ✅ Yes | ❌ No | ⚠️ Moderate |
| **!config (Interactive)** | **❌ No** | **✅ Yes** | **❌ No** | **✅ Yes** |

## Technical Details

### View Components
The configuration system uses two main Discord UI components:

1. **ConfigMenuView**: A View with buttons for different configuration categories
2. **OpenAIConfigModal**: A Modal form for inputting OpenAI settings

### Configuration Changes
- Changes made through the OpenAI Config modal are immediately saved to `config.json`
- The bot's AI handler will use the new settings for subsequent requests
- No bot restart is required

### Limitations

Current limitations of the interactive configuration system:

1. **View-Only for Some Categories**: Characters, user characters, lorebooks, and presets are currently view-only through the menu
2. **Full Management Still Requires Commands**: For adding/deleting/editing characters and lorebooks, use the respective commands
3. **GUI Still Needed for Complex Operations**: Creating presets with multiple message blocks is easier through the GUI

## Future Enhancements

Potential future improvements to the interactive configuration system:

- Add/Edit/Delete characters through modals
- Preset management with select menus
- Lorebook entry management
- User character creation and editing
- Reconnection settings modification
- Token management through modal

## Troubleshooting

### "Missing Permissions" Error
**Problem**: You receive a permissions error when trying to use `!config`.
**Solution**: Ensure you have Administrator permissions in the Discord server.

### Menu Buttons Don't Respond
**Problem**: Clicking buttons doesn't do anything.
**Solution**: The menu has likely expired (3-minute timeout). Run `!config` again to create a new menu.

### Configuration Changes Not Applied
**Problem**: Changes made through the config modal don't seem to take effect.
**Solution**: Check the bot's console for any error messages. Verify that `config.json` was updated successfully.

## Related Commands

- `!settoken <token>` - Set Discord bot token via command
- `!setopenai <base_url> <api_key>` - Configure OpenAI via command
- `!characters` - List all characters via command
- `!lorebook list` - List lorebooks via command

## See Also

- [README.md](README.md) - Main documentation
- [PRESET_FEATURES.md](PRESET_FEATURES.md) - Presets and advanced features
- [LOREBOOK_GUIDE.md](LOREBOOK_GUIDE.md) - Lorebook system documentation
