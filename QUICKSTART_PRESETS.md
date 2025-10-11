# Quick Start Guide - New Features

This guide will help you quickly get started with the new Preset System, User Characters, and Chat features.

## 1. Quick Setup (5 minutes)

### Step 1: Launch the GUI
```bash
python gui.py
```

### Step 2: Create Your First Preset
1. Click the **Presets** tab
2. Leave default AI configuration or adjust:
   - Temperature: 0.7 (for balanced creativity)
   - Max Tokens: 4096
3. Click **+ Add New Block**
4. Set Role to "system"
5. Enter content: `You are a helpful and friendly assistant.`
6. In "Preset Name" field, enter: `friendly_assistant`
7. Click **Save Preset**
8. Click **Set as Active**

✅ You now have an active preset!

### Step 3: Create a User Character (Optional)
1. Click the **User Characters** tab
2. Fill in:
   - Character Name: `john`
   - Display Name: `John`
   - Description: `A curious explorer`
3. Click **Add User Character**

✅ You can now use this character in chat!

## 2. Testing in Discord (5 minutes)

### Start the Bot
```bash
python bot.py
```

### Try the Chat Command
In any Discord channel where the bot is present:

```
!chat john: "What's the weather like today?" looks outside the window
```

The bot will:
- Recognize your user character (John)
- Store this message in the channel's history
- Respond with context awareness
- Track the conversation for future messages

### Continue the Conversation
```
!chat john: "Thanks! Can you tell me more about clouds?"
```

The bot remembers your previous message about weather!

### Clear History (Admin only)
```
!clearchat
```

## 3. Advanced Preset Example (10 minutes)

Create a role-playing game preset:

1. Go to **Presets** tab
2. Configure AI settings:
   - Temperature: 1.2 (more creative)
   - Max Tokens: 8192
   - Response Length: 2048
3. Add multiple blocks:

**Block 1** (Role: system):
```
You are a Dungeon Master for a fantasy RPG game. Describe scenes vividly and create engaging adventures.
```

**Block 2** (Role: system):
```
Always describe the environment, potential dangers, and give players meaningful choices.
```

**Block 3** (Role: user):
```
I want to explore the ancient ruins.
```

**Block 4** (Role: assistant):
```
As you approach the crumbling stone archway, you notice strange runes glowing faintly in the twilight. The air grows colder, and you hear a distant rumbling from within. What do you do?
```

4. Save as: `rpg_dungeon_master`
5. Set as Active

Now when you chat, the AI will act as a Dungeon Master!

## 4. Multiple AI Configuration Scenarios

### Creative Writing (High Creativity)
- Temperature: 1.3
- Top P: 0.95
- Presence Penalty: ✓ Enabled, 0.6
- Frequency Penalty: ✓ Enabled, 0.3

### Technical Support (Focused & Precise)
- Temperature: 0.3
- Top P: 0.8
- Response Length: 512
- No penalties

### Casual Conversation (Balanced)
- Temperature: 0.8
- Top P: 0.9
- Presence Penalty: ✓ Enabled, 0.2
- Default other settings

## 5. Common Workflows

### Workflow 1: Role-Playing Session
1. Create preset for game style (e.g., "dark_fantasy")
2. Set as active
3. Create user characters for each player
4. Players use `!chat character_name: actions/dialogue`
5. Bot responds as Game Master
6. History is automatically tracked
7. Use `!clearchat` to start new session

### Workflow 2: Story Development
1. Create preset with creative settings
2. Add example story snippets as blocks
3. Use `!chat` to develop plot
4. History builds the narrative
5. Export chat history from config.json if needed

### Workflow 3: Quick Q&A
1. Use default preset or simple system message
2. Set low temperature for factual responses
3. Use `!ask` for one-off questions
4. Use `!chat` when follow-up context matters

## 6. Tips & Tricks

### Tip 1: Test Block Toggles
- Create blocks for different scenarios
- Toggle them on/off to test different combinations
- No need to delete and recreate

### Tip 2: Character Name Shortcuts
- Use short, memorable names: `dm`, `alice`, `tech`
- Lowercase preferred for consistency
- Display names can be fancy

### Tip 3: Manage Context Window
- Use `!clearchat` to prevent token limit issues
- History limited to last 20 messages automatically
- Start fresh topics with clear history

### Tip 4: Preset Library
Create presets for different needs:
- `technical` - Low temp, precise
- `creative` - High temp, varied
- `rpg` - Medium temp, with examples
- `casual` - Balanced settings

### Tip 5: Combine Features
- Active preset sets overall behavior
- Character adds specific personality
- User characters identify speakers
- All work together seamlessly

## 7. Troubleshooting Quick Fixes

**Bot not using preset?**
→ Click "Set as Active" in Presets tab

**Chat history not working?**
→ Use `!chat` not just regular messages

**Preset changes not applying?**
→ Save preset first, then set as active

**Getting "character not found"?**
→ Check spelling, character names are case-insensitive but must match exactly

**Token limit errors?**
→ Reduce max_tokens or use `!clearchat` to reduce context

## 8. Next Steps

1. **Read Full Documentation**: See [PRESET_FEATURES.md](PRESET_FEATURES.md)
2. **Experiment**: Try different temperature and penalty values
3. **Share Presets**: Export your config.json presets section
4. **Build Character Library**: Create characters for your community
5. **Organize Channels**: Use different presets in different Discord channels

## Example: Complete Setup in 2 Minutes

```bash
# 1. Start GUI
python gui.py

# In GUI:
# - Go to Presets tab
# - Click "Add New Block"
# - Role: system, Content: "You are a helpful assistant"
# - Preset Name: "default"
# - Click "Save Preset"
# - Click "Set as Active"

# 2. Start bot
python bot.py

# In Discord:
# !chat "Hello! How are you today?"
```

That's it! You're now using the advanced preset system with chat tracking.

---

**Need Help?** Check [PRESET_FEATURES.md](PRESET_FEATURES.md) for detailed documentation.

**Have Issues?** Start with simple setups and gradually add complexity.
