# Visual Guide - Updated Features

## Configuration Tab Updates

### New Model Selection Feature

The Configuration tab now includes model selection:

```
┌─────────────────────────────────────────────────────────────────┐
│  OpenAI Compatible API Configuration                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Base URL:  [https://api.openai.com/v1________________]        │
│                                                                  │
│  API Key:   [**********************************_______]        │
│                                                                  │
│  Model:     [gpt-3.5-turbo                    ▼] [Fetch Models] │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**How to Use**:
1. Enter your API Base URL and API Key
2. Click **"Fetch Models"** button
3. Available models are pulled from your API
4. Select your preferred model from the dropdown
5. Click **"Save Configuration"**

The selected model is now used for all !chat responses.

---

## Manual Send Tab Updates

### Automatic ID Restoration

The Manual Send tab now remembers your last used Server ID and Channel ID:

```
┌─────────────────────────────────────────────────────────────────┐
│  Target Configuration                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Server ID:   [123456789012345678_______________]               │
│               ↑ Auto-filled from last use                       │
│                                                                  │
│  Channel ID:  [987654321098765432_______________]               │
│               ↑ Auto-filled from last use                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**What Changed**:
- ✅ Last used Server ID and Channel ID are saved
- ✅ Automatically restored when you open the GUI
- ✅ No need to re-enter IDs every time

### Direct Message Sending (No AI)

Manual Send now works differently:

**BEFORE** (with AI processing):
```
Your Message → AI Processing → AI Response → Discord
```

**AFTER** (direct sending):
```
Your Message → Discord (as-is)
```

**What This Means**:
- ✅ Messages are sent exactly as you type them
- ✅ No AI processing or modification
- ✅ Appears as a message from the selected character
- ✅ No model configuration required
- ✅ Faster (no API call delay)

---

## Configuration File Updates

### New Structure

Your `config.json` now includes:

```json
{
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "sk-...",
    "model": "gpt-4",                    ← NEW: Selected model
    "available_models": [                ← NEW: Cached models
      "gpt-3.5-turbo",
      "gpt-4",
      "gpt-4-turbo"
    ]
  },
  "last_manual_send": {                  ← NEW: Last used IDs
    "server_id": "123456789012345678",
    "channel_id": "987654321098765432"
  }
}
```

---

## Usage Examples

### Example 1: Setting Up Model Selection

1. Open GUI: `python gui.py`
2. Go to **Configuration** tab
3. Enter your API credentials
4. Click **"Fetch Models"**
5. Wait for models to load (you'll see a success message)
6. Select your preferred model (e.g., "gpt-4")
7. Click **"Save Configuration"**

Now all !chat responses will use your selected model!

### Example 2: Using Manual Send

1. Go to **Manual Send** tab
2. Server ID and Channel ID auto-fill from last use
3. Select a character (e.g., "Assistant")
4. Type your message:
   ```
   Hello everyone! This is a test message.
   ```
5. Click **"Send Message"**

The message appears in Discord exactly as typed, from the Assistant character.

### Example 3: Changing Models

Want to switch from GPT-3.5 to GPT-4?

1. **Configuration** tab
2. Click **"Fetch Models"** (if not already fetched)
3. Select "gpt-4" from dropdown
4. Click **"Save Configuration"**

Done! All future !chat commands use GPT-4.

---

## Troubleshooting

### "No models found" when fetching

**Cause**: API credentials may be incorrect or API doesn't support model listing

**Solution**:
1. Double-check Base URL and API Key
2. Click "Test OpenAI Connection" first
3. If test passes but fetch fails, manually type your model name (e.g., "gpt-3.5-turbo")
4. Save configuration

### Manual Send not working

**Before**: You got "Model not found" errors
**Now**: Works without any model configuration

If still having issues:
1. Check Discord bot token is configured
2. Verify Server ID and Channel ID are correct (numeric IDs)
3. Ensure character exists in Characters tab

### Last IDs not saving

**Check**:
1. Configuration file is writable
2. You're clicking "Send Message" (IDs save on send)
3. Restart GUI to see if IDs persist

---

## API Compatibility

### Fetch Models Support

The "Fetch Models" feature uses the OpenAI `/models` endpoint. This works with:

✅ OpenAI API
✅ Azure OpenAI (with proper configuration)
✅ LocalAI
✅ Most OpenAI-compatible APIs

If your API doesn't support model listing:
- You can still manually type the model name
- Save it in configuration
- It will work fine for !chat commands

---

## Benefits Summary

### Before Updates
- ❌ Manual Send required AI/model configuration
- ❌ Manual Send processed messages through AI
- ❌ Had to re-enter Server/Channel IDs every time
- ❌ Model was hardcoded, no selection
- ❌ "Model not found" errors

### After Updates
- ✅ Manual Send works without AI configuration
- ✅ Manual Send sends messages directly (as-is)
- ✅ Server/Channel IDs remembered automatically
- ✅ Model selection with dropdown
- ✅ "Fetch Models" button for convenience
- ✅ No more "Model not found" errors

---

## Screenshots

### Configuration Tab with Model Selection
See: `/tmp/config_with_model.png`

Shows the new Model dropdown and Fetch Models button in the Configuration tab.

---

For complete documentation, see:
- **UPDATE_SUMMARY.md** - Technical details of changes
- **PRESET_FEATURES.md** - Complete feature guide
- **QUICKSTART_PRESETS.md** - Quick start guide
