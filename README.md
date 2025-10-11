# Preset-Bot.
Rebuild Attempt - Stable AI Response and Manual Send Features

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

### 2. Manual Send
- Send messages directly to Discord channels
- Requires Server ID and Channel ID
- Character selection from configured characters
- AI generates responses based on your input and selected character

### 3. Discord Bot Configuration
- Secure token storage in config file
- Easy token management through GUI or config file

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Crazy-Rain/Preset-Bot..git
cd Preset-Bot.
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Option 1: Run the GUI: `python gui.py`
   - Option 2: Edit `config.json` manually (created from `config_template.json`)

## Usage

### GUI Mode (Recommended)
Run the GUI interface for easy configuration and manual message sending:
```bash
python gui.py
```

The GUI provides three tabs:
1. **Configuration**: Set Discord token and OpenAI API settings
2. **Manual Send**: Send messages to Discord channels with AI responses
3. **Characters**: Manage AI character personalities

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
- `!manualsend <server_id> <channel_id> <character> <message>` - Send manual message (Admin only)
- `!ask [character] <message>` - Ask the AI a question

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
  ]
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

## Security Notes
- `config.json` is excluded from version control (.gitignore)
- Never share your Discord token or API keys
- Store credentials securely

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)