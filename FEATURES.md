# Preset Bot - Features Documentation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Preset Discord Bot                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │   GUI Interface │         │   Bot Commands  │           │
│  │    (gui.py)     │         │    (bot.py)     │           │
│  └────────┬────────┘         └────────┬────────┘           │
│           │                           │                     │
│           └───────────┬───────────────┘                     │
│                       │                                     │
│              ┌────────▼────────┐                           │
│              │  ConfigManager  │                           │
│              │  (config.json)  │                           │
│              └────────┬────────┘                           │
│                       │                                     │
│         ┌─────────────┼─────────────┐                     │
│         │             │             │                     │
│    ┌────▼───┐   ┌────▼────┐   ┌────▼────┐               │
│    │Discord │   │ OpenAI  │   │Character│               │
│    │ Token  │   │   API   │   │  System │               │
│    └────────┘   └─────────┘   └─────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Feature 1: AI Response Function

### Configuration Storage
All AI configuration is stored in `config.json`:

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",  // OpenAI compatible endpoint
    "api_key": "your-api-key-here"             // API authentication key
  }
}
```

### Usage Methods

#### Method 1: GUI Configuration
1. Run `python gui.py`
2. Go to "Configuration" tab
3. Fill in:
   - **Base URL**: Your OpenAI compatible API endpoint
   - **API Key**: Your API authentication key
4. Click "Save Configuration"
5. Click "Test OpenAI Connection" to verify

#### Method 2: Bot Command
```
!setopenai <base_url> <api_key>
```
Example:
```
!setopenai https://api.openai.com/v1 sk-abc123xyz789
```

#### Method 3: Direct Config Edit
Edit `config.json` manually and restart the bot.

### Supported API Providers
- OpenAI (https://api.openai.com/v1)
- Azure OpenAI (https://YOUR-RESOURCE.openai.azure.com/)
- LocalAI (http://localhost:8080/v1)
- Any OpenAI-compatible API endpoint

---

## Feature 2: Manual Send

### Components Required
1. **Message**: The text you want to send to the AI
2. **Server ID**: Discord server (guild) ID where the channel is located
3. **Channel ID**: Specific Discord channel ID to send to
4. **Character**: AI personality to use for the response

### Usage Methods

#### Method 1: GUI Interface (Recommended)
1. Run `python gui.py`
2. Go to "Manual Send" tab
3. Fill in the fields:
   - **Server ID**: Right-click on server → Copy ID (enable Developer Mode)
   - **Channel ID**: Right-click on channel → Copy ID
   - **Character**: Select from dropdown
   - **Message**: Type your message in the text box
4. Click "Send Message"

The bot will:
1. Generate an AI response using your message and selected character
2. Send the response to the specified Discord channel

#### Method 2: Bot Command
```
!manualsend <server_id> <channel_id> <character> <message>
```
Example:
```
!manualsend 123456789 987654321 Assistant Write a poem about coding
```

#### Method 3: Programmatic (Python Script)
Use the `example_manual_send.py` script:

```python
from bot import ConfigManager, AIResponseHandler
import asyncio

async def send():
    config_mgr = ConfigManager()
    ai_handler = AIResponseHandler(config_mgr)
    
    # Generate AI response
    response = await ai_handler.get_ai_response(
        "Your message here",
        character_name="Assistant"
    )
    
    # Send to Discord channel
    # ... (see example_manual_send.py for full code)

asyncio.run(send())
```

---

## Feature 3: Discord Bot Token

### Configuration Storage
The Discord bot token is securely stored in `config.json`:

```json
{
  "discord": {
    "token": "your-bot-token-here"
  }
}
```

### How to Get a Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select existing
3. Go to "Bot" section in the left sidebar
4. Click "Reset Token" to generate a new token
5. Copy the token (you won't be able to see it again!)
6. Enable necessary intents:
   - Message Content Intent (required for reading messages)
   - Server Members Intent (optional, for member info)

### Setting the Token

#### Method 1: GUI
1. Run `python gui.py`
2. Go to "Configuration" tab
3. Paste token in "Bot Token" field
4. Click "Save Configuration"

#### Method 2: Bot Command (requires existing token)
```
!settoken <your-bot-token>
```
**Note**: This command requires the bot to already be running with a token.

#### Method 3: Direct Config Edit
1. Copy `config_template.json` to `config.json`
2. Edit `config.json`:
   ```json
   {
     "discord": {
       "token": "paste-your-token-here"
     }
   }
   ```
3. Save and run the bot

---

## Character System

### What are Characters?
Characters define different AI personalities with unique system prompts.

### Managing Characters

#### Adding Characters via GUI
1. Run `python gui.py`
2. Go to "Characters" tab
3. Fill in:
   - **Character Name**: e.g., "HelperBot", "TechExpert", "FriendlyAssistant"
   - **System Prompt**: Instructions for the AI's behavior
4. Click "Add Character"

#### Adding Characters via Bot Command
```
!addcharacter <name> <system_prompt>
```
Example:
```
!addcharacter TechExpert You are an expert in technology and programming. You provide detailed technical explanations.
```

#### Listing Characters
- GUI: See the list in "Characters" tab
- Bot Command: `!characters`

### Example Characters

```json
{
  "characters": [
    {
      "name": "Assistant",
      "system_prompt": "You are a helpful assistant."
    },
    {
      "name": "TechSupport",
      "system_prompt": "You are a technical support specialist. Provide clear, step-by-step solutions to technical problems."
    },
    {
      "name": "CreativeWriter",
      "system_prompt": "You are a creative writer. Write engaging, imaginative, and descriptive content."
    },
    {
      "name": "Tutor",
      "system_prompt": "You are an educational tutor. Explain concepts clearly with examples and encourage learning."
    }
  ]
}
```

---

## Quick Start Guide

### First Time Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your credentials**:
   - Discord bot token (from Discord Developer Portal)
   - OpenAI API key (from OpenAI or compatible provider)

3. **Configure the bot**:
   ```bash
   python gui.py
   ```
   Or use the quick start menu:
   ```bash
   python start.py
   ```

4. **Test the setup**:
   - In GUI: Click "Test OpenAI Connection"
   - Verify all fields are filled

5. **Start using**:
   - For manual sends: Use the "Manual Send" tab in GUI
   - For bot commands: Run `python bot.py` in a separate terminal

### Getting Discord IDs
Enable Developer Mode in Discord:
1. User Settings → Advanced → Developer Mode (toggle on)
2. Right-click on server → Copy ID
3. Right-click on channel → Copy ID

---

## Troubleshooting

### "Discord bot token not configured"
**Solution**: Set your Discord bot token in the Configuration tab.

### "OpenAI API not configured"
**Solution**: Set your OpenAI base URL and API key in the Configuration tab.

### "Channel not found"
**Solution**: 
- Verify the channel ID is correct
- Ensure the bot has access to that channel
- Check that the bot is in the server

### "Permission denied"
**Solution**: 
- Ensure the bot has necessary permissions in Discord
- Check that you have admin permissions for admin commands

### GUI won't start
**Solution**: 
- Make sure tkinter is installed (usually comes with Python)
- Use bot.py command-line interface instead
- Edit config.json manually

---

## Security Best Practices

1. **Never commit config.json** to version control
   - It's already in `.gitignore`
   - Contains sensitive tokens and keys

2. **Keep tokens secure**
   - Don't share in public channels
   - Regenerate if exposed

3. **Use environment variables** (optional)
   - Can be added as enhancement
   - Currently using config.json for simplicity

4. **Restrict admin commands**
   - Commands like `!settoken` require admin permissions
   - Only use in private/admin channels

---

## API Rate Limits

Be aware of rate limits:
- **OpenAI**: Varies by tier (check your dashboard)
- **Discord**: ~50 messages per second per channel

For high-volume usage, implement rate limiting in your code.

---

## Support & Documentation

- **Discord.py docs**: https://discordpy.readthedocs.io/
- **OpenAI docs**: https://platform.openai.com/docs/
- **Repository**: https://github.com/Crazy-Rain/Preset-Bot.

For issues or questions, please create an issue in the GitHub repository.
