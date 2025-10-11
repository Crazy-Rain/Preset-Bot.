# GUI Interface Documentation

## Overview
The Preset Bot GUI provides a user-friendly interface for configuring the bot and sending manual messages. The GUI is organized into three main tabs.

## Tab 1: Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│  Preset Discord Bot - Configuration & Manual Send         [_][□][×] │
├─────────────────────────────────────────────────────────────────┤
│  [Configuration] [Manual Send] [Characters]                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ Discord Configuration ─────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Bot Token:  [●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●] │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ OpenAI Compatible API Configuration ──────────────────────┐ │
│  │                                                              │ │
│  │  Base URL:  [https://api.openai.com/v1________________]    │ │
│  │                                                              │ │
│  │  API Key:   [●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●] │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  [Save Configuration] [Load Configuration] [Test OpenAI Connection] │
│                                                                   │
│  Configuration saved successfully!                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration Tab Features:
- **Discord Token Field**: Password-masked input for bot token
- **OpenAI Base URL**: Configure any OpenAI-compatible endpoint
- **OpenAI API Key**: Password-masked input for API key
- **Save Configuration**: Persists settings to config.json
- **Load Configuration**: Reloads from config.json
- **Test Connection**: Validates OpenAI API connection

---

## Tab 2: Manual Send

```
┌─────────────────────────────────────────────────────────────────┐
│  Preset Discord Bot - Configuration & Manual Send         [_][□][×] │
├─────────────────────────────────────────────────────────────────┤
│  [Configuration] [Manual Send] [Characters]                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ Target Configuration ──────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Server ID:   [123456789012345678__________________]       │ │
│  │                                                              │ │
│  │  Channel ID:  [987654321098765432__________________]       │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ Character Selection ───────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Character:  [Assistant ▼]                                  │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ Message ────────────────────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Write a short poem about the beauty of coding and         │ │
│  │  the elegance of well-written software.                    │ │
│  │                                                              │ │
│  │  ↕                                                           │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  [Send Message] [Clear]                                          │
│                                                                   │
│  Message sent successfully!                                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Manual Send Tab Features:
- **Server ID**: Enter Discord server (guild) ID
- **Channel ID**: Enter target channel ID
- **Character Dropdown**: Select from configured AI characters
- **Message Textbox**: Large scrollable text area for input
- **Send Message**: Generates AI response and sends to Discord
- **Clear**: Clears the message textbox

### How to Get IDs:
1. Enable Developer Mode: Discord Settings → Advanced → Developer Mode
2. Right-click on server → Copy ID
3. Right-click on channel → Copy ID

---

## Tab 3: Characters

```
┌─────────────────────────────────────────────────────────────────┐
│  Preset Discord Bot - Configuration & Manual Send         [_][□][×] │
├─────────────────────────────────────────────────────────────────┤
│  [Configuration] [Manual Send] [Characters]                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ Add New Character ─────────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Character Name:  [TechSupport___________________]          │ │
│  │                                                              │ │
│  │  System Prompt:                                             │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │You are a technical support specialist. Provide clear,  │ │ │
│  │  │step-by-step solutions to technical problems. Be        │ │ │
│  │  │patient and helpful.                                     │ │ │
│  │  │↕                                                        │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  │                                   [Add Character]           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ Current Characters ────────────────────────────────────────┐ │
│  │                                                              │ │
│  │  Assistant: You are a helpful assistant.                    │ │
│  │  TechSupport: You are a technical support specialist...    │ │
│  │  CreativeWriter: You are a creative writer. Write enga...  │ │
│  │  Tutor: You are an educational tutor. Explain conce...     │ │
│  │                                                              │ │
│  │  ↕                                                           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│                                        [Refresh List]            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Characters Tab Features:
- **Add Character Section**:
  - Character Name: Unique identifier for the character
  - System Prompt: Large text area for defining AI behavior
  - Add Character button: Saves to configuration
  
- **Current Characters List**:
  - Shows all configured characters
  - Displays name and prompt preview
  - Refresh button to reload from config

---

## Usage Workflow

### First Time Setup
1. Launch GUI: `python gui.py`
2. Go to **Configuration** tab
3. Enter Discord bot token
4. Enter OpenAI base URL and API key
5. Click "Save Configuration"
6. Click "Test OpenAI Connection" to verify

### Adding Characters
1. Go to **Characters** tab
2. Enter character name (e.g., "TechExpert")
3. Enter system prompt defining behavior
4. Click "Add Character"
5. Character now available in Manual Send dropdown

### Sending Manual Messages
1. Go to **Manual Send** tab
2. Enter Server ID and Channel ID
3. Select character from dropdown
4. Type your message
5. Click "Send Message"
6. Bot generates AI response and sends to Discord

---

## Command-Line Alternative

For users who prefer command-line or don't have GUI access:

### Quick Start Menu
```bash
$ python start.py

==================================================
  Preset Discord Bot - Quick Start Menu
==================================================

1. Run Configuration GUI
2. Run Discord Bot
3. Check Configuration
4. Exit

==================================================

Enter your choice (1-4): 
```

### Configuration Validation
```bash
$ python validate_config.py

============================================================
  Preset Bot - Configuration Validator
============================================================
✅ config.json loaded successfully

============================================================
Discord Configuration
============================================================
✅ Discord token is set (72 characters)

============================================================
OpenAI Configuration
============================================================
✅ Base URL: https://api.openai.com/v1
✅ API key is set (51 characters)

============================================================
Characters Configuration
============================================================
✅ 4 character(s) configured:
   ✅ Assistant: You are a helpful assistant.
   ✅ TechSupport: You are a technical support specialist...
   ✅ CreativeWriter: You are a creative writer. Write enga...
   ✅ Tutor: You are an educational tutor. Explain conce...

============================================================
Dependencies Check
============================================================
✅ discord is installed
✅ openai is installed

============================================================
Validation Summary
============================================================
✅ Discord Configuration
✅ OpenAI Configuration
✅ Characters Configuration
✅ Dependencies
============================================================

🎉 Configuration is valid!
   You can now run the bot with: python bot.py
   Or use the GUI with: python gui.py
```

---

## Bot Commands (When Running bot.py)

Once the bot is running (`python bot.py`), use these commands in Discord:

```
!settoken <token>
  Set Discord bot token (Admin only)

!setopenai <base_url> <api_key>
  Configure OpenAI API (Admin only)
  Example: !setopenai https://api.openai.com/v1 sk-abc123

!addcharacter <name> <system_prompt>
  Add new character (Admin only)
  Example: !addcharacter Helper You are a helpful assistant.

!characters
  List all available characters

!manualsend <server_id> <channel_id> <character> <message>
  Send manual message (Admin only)
  Example: !manualsend 123456 789012 Assistant Hello world

!ask [character] <message>
  Ask the AI a question
  Example: !ask Assistant What is Python?
  Example: !ask What is coding?
```

---

## Troubleshooting Guide

### GUI won't start
```
Error: No module named 'tkinter'
```
**Solution**: Use command-line interface instead
- Run: `python bot.py` for bot mode
- Edit `config.json` directly for configuration

### OpenAI Connection Test Fails
```
Error: Connection failed: 401 Unauthorized
```
**Solution**: 
- Verify API key is correct
- Check if you have API credits/quota
- Ensure base URL is correct

### Manual Send Fails
```
Error: Channel 123456 not found
```
**Solutions**:
- Verify channel ID is correct (right-click → Copy ID)
- Ensure bot is in the server
- Check bot has permission to send messages in that channel

### Bot Commands Don't Work
**Solutions**:
- Ensure bot is running: `python bot.py`
- Check bot has necessary permissions
- Admin commands require administrator role
- Verify command prefix is `!`

---

## Security Notes

⚠️ **Important Security Practices**

1. **Never share your config.json**
   - Contains sensitive tokens and API keys
   - Already excluded from git via .gitignore

2. **Protect your tokens**
   - Don't post screenshots showing tokens
   - Regenerate if accidentally exposed

3. **Use secure channels**
   - Only use admin commands in private channels
   - Be careful with manual send to public channels

4. **Monitor API usage**
   - Check OpenAI usage dashboard regularly
   - Set up billing alerts

---

## Support

For issues or questions:
- Check `FEATURES.md` for detailed documentation
- Run `python validate_config.py` to diagnose configuration issues
- Review `README.md` for installation and usage guide
- Create an issue on GitHub: https://github.com/Crazy-Rain/Preset-Bot.
