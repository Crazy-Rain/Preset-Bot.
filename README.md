# Preset-Bot.
Rebuild Attempt - Stable AI Response and Manual Send Features

## Quick Start

Get started in 3 simple steps:

```bash
# 1. Install dependencies
npm install

# 2. Launch the bot
npm start

# 3. Follow the interactive menu to configure and run
```

## Overview
This is a Discord bot with AI response capabilities and manual send features. The bot supports:
- **OpenAI Compatible API Integration**: Configure any OpenAI-compatible API endpoint
- **Manual Send**: Send messages directly to Discord channels with AI-generated responses
- **Character System**: Create and manage different AI characters with custom system prompts
- **GUI Interface**: User-friendly interface for configuration and manual message sending

## Features

### 1. AI Response Function
- OpenAI compatible API configuration with customizable BASE URL and API KEY
- Supports any OpenAI-compatible endpoint (OpenAI, Azure OpenAI, LocalAI, etc.)
- Configuration saved to `config.json`

### 2. Preset System (NEW!)
- Advanced AI configuration with multiple message blocks
- Fine-tune AI behavior: temperature, top_p, reasoning, penalties
- Save and load different presets for different scenarios
- Active/Inactive blocks for easy testing

### 3. User Characters (NEW!)
- Create character profiles for users/players
- Use with `!chat` command for role-playing
- Avatar support (URL or file upload)

### 4. Chat System (NEW!)
- `!chat` command for tracked conversations
- Per-channel message history
- Context-aware responses using last 20 messages
- Integrates with User Characters

### 5. Lorebook System (NEW!)
- Create contextual information repositories
- Active/Inactive toggle per lorebook
- **Constant entries**: Always included in AI context
- **Normal entries**: Triggered by keywords in messages
- **Bulk Import**: Import lorebook entries from JSON files (NEW!)
- Perfect for world-building, character lore, and campaign tracking
- Similar to SillyTavern's lorebook functionality

### 6. Manual Send
- Send messages directly to Discord channels
- Requires Server ID and Channel ID
- Character selection from configured characters
- AI generates responses based on your input and selected character

### 7. Discord Bot Configuration
- Secure token storage in config file
- Easy token management through GUI or config file

### 8. Character System
- Create and manage different AI characters with custom system prompts
- Avatar support for characters (URL or local file)
- Webhook integration for character identity in Discord

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Crazy-Rain/Preset-Bot..git
cd Preset-Bot.
```

2. Install dependencies (choose one method):

   **Option A: Using npm (Recommended)**
   ```bash
   npm install
   ```

   **Option B: Using pip directly**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** If running as a startup application, `start.py` will automatically check and install missing dependencies when launched.

3. Configure the bot:
   - Option 1: Run the GUI: `python gui.py`
   - Option 2: Edit `config.json` manually (created from `config_template.json`)

## Usage

### Quick Start (Easiest Methods)

**Option 1: Using npm start**
```bash
npm start
```
This launches an interactive menu where you can choose to run the GUI, bot, or check configuration.

**Option 2: Using start.sh script**
```bash
./start.sh
```
This provides an interactive menu with the following options:
1. Run Configuration GUI
2. Run Discord Bot
3. Check Configuration Status
4. Run Interactive Start Menu
5. Exit

You can also use direct commands:
```bash
./start.sh gui          # Launch GUI directly
./start.sh bot          # Start the bot directly
./start.sh check        # Check configuration
./start.sh interactive  # Launch interactive menu
```

**Option 3: Using npm scripts**
```bash
npm run gui             # Run Configuration GUI
npm run bot             # Run Discord Bot
npm run check-config    # Check configuration status
npm test                # Run tests
```

### GUI Mode (Recommended)
Run the GUI interface for easy configuration and manual message sending:
```bash
python gui.py
```

The GUI provides five tabs:
1. **Configuration**: Set Discord token and OpenAI API settings
2. **Presets**: Configure AI behavior with advanced options and message blocks
3. **Manual Send**: Send messages to Discord channels with AI responses
4. **Characters**: Manage AI character personalities
5. **User Characters**: Manage user/player character profiles for chat
6. **Lorebooks**: Create and manage lorebooks, import from JSON files (NEW!)

### Bot Mode
Run the Discord bot with commands:
```bash
python bot.py
```

Available commands:
- `!settoken <token>` - Set Discord bot token (Admin only)
- `!setopenai <base_url> <api_key>` - Configure OpenAI API (Admin only)
- `!addcharacter <name> <system_prompt>` - Add new character (Admin only)
- `!characters` - List all characters
- `!character <name>` - Set channel-specific character (NEW!)
- `!manualsend <server_id> <channel_id> <character> <message>` - Send manual message (Admin only)
- `!ask [character] <message>` - Ask the AI a question
- `!chat [character]: <message>` - Chat with context tracking (NEW!)
- `!clearchat` - Clear chat history for current channel (Admin only, NEW!)
- `!set <character_name>` - Manually set your active user character (NEW!)
- `!viewu [character_name]` - View your current user character (NEW!)
- `!viewc [character_name]` - View current AI character for the channel (NEW!)
- `!image <character> <url>` - Update AI character avatar
- `!cimage <character> <url>` - Update user character avatar (NEW!)
- `!lorebook <action> [args]` - Manage lorebooks (NEW!)
  - `create <name>` - Create a new lorebook
  - `list` - List all lorebooks
  - `activate <name>` - Activate a lorebook
  - `deactivate <name>` - Deactivate a lorebook
  - `show <name>` - Show lorebook entries
  - `addentry <name> <constant|normal> <content> [keywords...]` - Add entry
  - `delentry <name> <index>` - Delete entry
  - `delete <name>` - Delete lorebook

## Configuration

### config.json Structure
```json
{
  "discord": {
    "token": "YOUR_DISCORD_BOT_TOKEN"
  },
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "YOUR_OPENAI_API_KEY"
  },
  "characters": [
    {
      "name": "Assistant",
      "system_prompt": "You are a helpful assistant."
    }
  ],
  "user_characters": [],
  "presets": [],
  "active_preset": null,
  "chat_history": {},
  "lorebooks": []
}
```

### Getting Required Credentials

#### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Click "Reset Token" to get your bot token
5. Enable necessary intents (Message Content Intent)

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API keys section
3. Create a new API key

For alternative OpenAI-compatible endpoints, use their respective base URL and API key.

## Directory Structure
```
Preset-Bot./
├── bot.py                  # Main Discord bot application
├── gui.py                  # GUI interface for configuration and manual send
├── config.json             # Configuration file (created at runtime)
├── config_template.json    # Template for configuration
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Advanced Features

For detailed information about the new features, see:
- **[LAUNCH_GUIDE.md](LAUNCH_GUIDE.md)** - Comprehensive guide for all launch methods (NEW!)
- **[PRESET_FEATURES.md](PRESET_FEATURES.md)** - Comprehensive guide to presets, user characters, and chat system
- **[LOREBOOK_GUIDE.md](LOREBOOK_GUIDE.md)** - Complete lorebook documentation with examples
- **[LOREBOOK_IMPORTER_GUIDE.md](LOREBOOK_IMPORTER_GUIDE.md)** - Guide to bulk importing lorebook entries (NEW!)
- **[LOREBOOK_QUICK_REFERENCE.md](LOREBOOK_QUICK_REFERENCE.md)** - Quick command reference for lorebooks
- **[NEW_COMMANDS_GUIDE.md](NEW_COMMANDS_GUIDE.md)** - Guide for !viewu, !viewc, and !cimage commands (NEW!)

## Security Notes
- `config.json` is excluded from version control (.gitignore)
- Never share your Discord token or API keys
- Store credentials securely

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)