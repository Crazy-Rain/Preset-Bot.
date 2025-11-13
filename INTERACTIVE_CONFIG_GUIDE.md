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
Opens the **Interactive AI Character Management** interface with full control over AI characters:
- **Select Character**: Dropdown menu to select a character for operations
- **Create Character**: Create new AI characters with system prompts and avatars
- **View Details**: See full character information including system prompts and avatars
- **Delete Character**: Remove an AI character with confirmation dialog

**NEW!** AI characters can now be fully managed through Discord without command-line syntax.

#### 👥 User Characters
Opens the **Interactive User Character Management** interface with full control over user/player characters:
- **Select Character**: Dropdown menu to select a character for operations
- **Create User Character**: Create new user/player characters with descriptions and avatars
- **View Details**: See full character information including descriptions and avatars
- **Delete Character**: Remove a user character with confirmation dialog

**NEW!** User characters can now be fully managed through Discord without command-line syntax.

#### ⚙️ Bot Settings
Displays current bot configuration including:
- **Reconnection Settings**:
  - Enabled/Disabled status
  - Maximum retry attempts
  - Base delay between retries
  - Maximum delay between retries

#### 📚 Lorebooks
Opens the **Interactive Lorebook Management** interface with full control over lorebooks:
- **Select Lorebook**: Dropdown menu to select a lorebook for operations
- **Create Lorebook**: Create new lorebooks with a unique name
- **Toggle Active/Inactive**: Enable or disable selected lorebook
- **Add Entry**: Add new constant or normal entries with keywords
- **View Entries**: See all entries in the selected lorebook (paginated)
- **Delete Lorebook**: Remove a lorebook with confirmation dialog

**NEW!** Lorebooks can now be fully managed through Discord without command-line syntax or accessing the host machine.

#### 🎯 Presets
Shows all AI presets with:
- Preset names
- Active preset indicator (⭐)
- Number of message blocks in each preset

#### ❌ Close
Closes the configuration menu.

## Usage Examples

### Managing Lorebooks Interactively (NEW!)

1. Type `!config` in Discord
2. Click the "📚 Lorebooks" button
3. You'll see the Lorebook Management interface

**To Create a New Lorebook:**
- Click "➕ Create Lorebook"
- Enter a unique name in the modal
- Click "Submit"
- The lorebook is created and automatically activated

**To Toggle a Lorebook Active/Inactive:**
- Select a lorebook from the dropdown menu
- Click "🔄 Toggle Active/Inactive"
- The status will be toggled instantly

**To Add an Entry:**
- Select a lorebook from the dropdown menu
- Click "📝 Add Entry"
- Fill in the modal form:
  - **Entry Content**: The text to inject into conversations
  - **Entry Type**: Either "constant" (always active) or "normal" (keyword-triggered)
  - **Keywords**: Comma-separated keywords (only for normal entries)
- Click "Submit"

**To View Entries:**
- Select a lorebook from the dropdown menu
- Click "👁️ View Entries"
- See all entries with their types, content, and keywords (first 10 shown)

**To Delete a Lorebook:**
- Select a lorebook from the dropdown menu
- Click "🗑️ Delete Lorebook"
- Confirm deletion in the dialog
- The lorebook and all its entries will be removed

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

### Managing AI Characters Interactively (NEW!)

1. Type `!config` in Discord
2. Click the "🤖 Characters" button
3. You'll see the AI Character Management interface

**To Create a New AI Character:**
- Click "➕ Create Character"
- Fill in the modal form:
  - **Character Name**: Internal identifier (e.g., "assistant", "narrator")
  - **Display Name**: Name shown in Discord
  - **System Prompt/Description**: The AI's personality and behavior instructions
  - **Avatar URL**: Optional image URL for the character
- Click "Submit"
- The character is created instantly

**To View Character Details:**
- Select a character from the dropdown menu
- Click "👁️ View Details"
- See full information including system prompt and avatar

**To Delete a Character:**
- Select a character from the dropdown menu
- Click "🗑️ Delete Character"
- Confirm deletion in the dialog

### Managing User Characters Interactively (NEW!)

1. Type `!config` in Discord
2. Click the "👥 User Characters" button
3. You'll see the User Character Management interface

**To Create a New User Character:**
- Click "➕ Create User Character"
- Fill in the modal form:
  - **Character Name**: Internal identifier (e.g., "john", "alice")
  - **Display Name**: Name shown in Discord
  - **Character Description**: Background and personality of the character
  - **Avatar URL**: Optional image URL for the character
- Click "Submit"
- The character is created instantly

**To View/Delete User Characters:**
- Same workflow as AI characters using the dropdown menu and buttons

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
The configuration system uses multiple Discord UI components:

1. **ConfigMenuView**: A View with buttons for different configuration categories
2. **OpenAIConfigModal**: A Modal form for inputting OpenAI settings
3. **LorebookManagementView**: Interactive view for managing lorebooks (NEW!)
4. **CreateLorebookModal**: Modal form for creating new lorebooks (NEW!)
5. **AddLorebookEntryModal**: Modal form for adding lorebook entries (NEW!)
6. **ConfirmDeleteView**: Confirmation dialog for deleting lorebooks (NEW!)
7. **CharacterManagementView**: Interactive view for managing AI characters (NEW!)
8. **UserCharacterManagementView**: Interactive view for managing user characters (NEW!)
9. **CreateCharacterModal**: Modal form for creating AI characters (NEW!)
10. **CreateUserCharacterModal**: Modal form for creating user characters (NEW!)
11. **ConfirmCharacterDeleteView**: Confirmation dialog for deleting characters (NEW!)
12. **ConfirmUserCharacterDeleteView**: Confirmation dialog for deleting user characters (NEW!)

### Configuration Changes
- Changes made through modals are immediately saved to `config.json`
- The bot's AI handler will use the new settings for subsequent requests
- No bot restart is required
- Lorebook and character changes take effect immediately in ongoing conversations

### Limitations

Current limitations of the interactive configuration system:

1. **View-Only for Presets**: Presets are currently view-only through the menu
2. **Full Management for Lorebooks**: ✅ Lorebooks can now be fully managed interactively! (NEW!)
3. **Full Management for Characters**: ✅ AI and User characters can now be fully managed interactively! (NEW!)
4. **GUI Still Needed for Complex Operations**: Creating presets with multiple message blocks is easier through the GUI
5. **Character Editing**: Characters can be created and deleted but not edited yet (coming soon!)

## Future Enhancements

Potential future improvements to the interactive configuration system:

- Edit existing AI and user characters through modals
- Preset management with select menus
- ~~Lorebook entry management~~ ✅ **COMPLETED!**
- ~~AI character creation and deletion~~ ✅ **COMPLETED!**
- ~~User character creation and deletion~~ ✅ **COMPLETED!**
- Reconnection settings modification
- Token management through modal
- Delete individual lorebook entries interactively
- Batch operations for multiple items

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

### Lorebook Management Issues (NEW!)

**Problem**: "Please select a lorebook first using the dropdown menu."
**Solution**: Make sure to click on a lorebook in the dropdown menu at the top before using buttons like Toggle, Add Entry, View Entries, or Delete.

**Problem**: Cannot create a lorebook with the same name.
**Solution**: Lorebook names must be unique. Choose a different name or delete the existing lorebook first.

**Problem**: Keywords not working for normal entries.
**Solution**: Ensure keywords are comma-separated (e.g., "dragon, dragons, drake"). Keywords are case-insensitive and match partial words.

**Problem**: Entry content is truncated when viewing.
**Solution**: The view shows truncated content to fit Discord's embed limits. Use `!lorebook show <name>` command to see full content of all entries.

## Related Commands

- `!settoken <token>` - Set Discord bot token via command
- `!setopenai <base_url> <api_key>` - Configure OpenAI via command
- `!characters` - List all characters via command
- `!lorebook list` - List lorebooks via command

## See Also

- [README.md](README.md) - Main documentation
- [PRESET_FEATURES.md](PRESET_FEATURES.md) - Presets and advanced features
- [LOREBOOK_GUIDE.md](LOREBOOK_GUIDE.md) - Lorebook system documentation
