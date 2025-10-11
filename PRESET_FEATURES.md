# Preset System and Chat Features Documentation

## New Features Overview

This update adds several major features to the Preset Bot:

1. **Preset System** - Advanced AI configuration with message blocks
2. **User Characters** - Character profiles for users/players in chat
3. **Chat System** - Channel-based conversation tracking with `!chat` command
4. **AI Configuration Options** - Fine-tune AI behavior with multiple parameters

---

## 1. Preset System

### What are Presets?

Presets allow you to configure advanced AI behavior including:
- Multiple message blocks (system/user/assistant messages)
- AI model parameters (temperature, top_p, etc.)
- Context and response length limits
- Reasoning settings
- Presence and frequency penalties

### Using Presets in the GUI

1. Open the **Presets** tab in the GUI
2. Configure AI settings in the "AI Configuration Options" section
3. Add message blocks with the "+ Add New Block" button
4. Save your preset with a name
5. Set it as active to use in conversations

### AI Configuration Options

| Option | Description | Range/Values |
|--------|-------------|--------------|
| **Max Tokens / Context Length** | Maximum context window | 1 - 2,000,000 |
| **Response Length** | Max tokens in response | Any positive integer |
| **Temperature** | Randomness in responses | 0.0 - 2.0 |
| **Top P** | Nucleus sampling threshold | 0.0 - 1.0 |
| **Model Reasoning** | Enable reasoning capabilities | Checkbox |
| **Reasoning Level** | How much reasoning to use | Auto, Maximum, High, Medium, Low, Minimum |
| **Presence Penalty** | Penalty for repeating topics | -2.0 - 2.0 (toggle to enable) |
| **Frequency Penalty** | Penalty for repeating words | -2.0 - 2.0 (toggle to enable) |

### Message Blocks

Each preset can have multiple message blocks. Each block has:
- **Active** checkbox - Enable/disable this block
- **Role** - Who sends this message (system/user/assistant)
- **Content** - The message content

**Example Use Cases:**
- Multiple system messages to define different aspects of behavior
- Example user/assistant exchanges to demonstrate desired conversation style
- Different prompts for different scenarios

### Preset Structure (config.json)

```json
{
  "presets": [
    {
      "name": "creative_writer",
      "ai_config": {
        "max_tokens": 4096,
        "response_length": 1024,
        "temperature": 1.2,
        "top_p": 0.9,
        "reasoning_enabled": false,
        "reasoning_level": "Auto",
        "use_presence_penalty": true,
        "presence_penalty": 0.6,
        "use_frequency_penalty": true,
        "frequency_penalty": 0.3
      },
      "blocks": [
        {
          "active": true,
          "role": "system",
          "content": "You are a creative writer with a vivid imagination."
        },
        {
          "active": true,
          "role": "system",
          "content": "Always write in an engaging, descriptive style."
        }
      ]
    }
  ],
  "active_preset": "creative_writer"
}
```

### Managing Presets

- **Save Preset** - Save current configuration with a name
- **Load Preset** - Load a saved preset into the editor
- **Set as Active** - Make this preset the default for AI responses

---

## 2. User Characters

### What are User Characters?

User Characters are profiles that users/players can use when chatting with the `!chat` command. Unlike AI Characters (which the bot uses to respond), User Characters represent the people chatting.

### Adding User Characters in the GUI

1. Go to the **User Characters** tab
2. Fill in:
   - **Character Name (ID)** - Lowercase identifier (e.g., `alice`)
   - **Display Name** - Name shown in chat (e.g., `Alice`)
   - **Description** - Character background/personality
   - **Avatar** - URL or upload a file
3. Click "Add User Character"

### User Character Structure

```json
{
  "user_characters": [
    {
      "name": "alice",
      "display_name": "Alice",
      "description": "A brave adventurer who loves exploring dungeons.",
      "avatar_url": "https://example.com/alice.png",
      "avatar_file": "character_avatars/user_alice.png"
    }
  ]
}
```

---

## 3. Chat System

### The !chat Command

The `!chat` command allows users to have conversations that are tracked per channel, with optional character assignment.

**Usage:**
```
!chat [character_name]: "dialogue" action description
```

**Examples:**
```
!chat Alice: "Hello there!" waves enthusiastically
!chat Bob: "Nice to meet you, Alice." extends hand for a handshake
!chat "What do you think about this?" looks around curiously
```

### How It Works

1. **Message Tracking** - All `!chat` messages are tracked per channel
2. **Context Awareness** - The AI sees the last 20 messages for context
3. **Character Integration** - User characters are identified in the conversation
4. **Persistent History** - Chat history is saved in config.json

### Chat History Structure

```json
{
  "chat_history": {
    "123456789": [
      {
        "author": "987654321",
        "author_name": "JohnDoe",
        "user_character": "alice",
        "content": "Hello there!",
        "type": "user",
        "timestamp": "2025-10-11T08:00:00.000000"
      },
      {
        "content": "Hello Alice! How can I help you today?",
        "type": "assistant",
        "timestamp": "2025-10-11T08:00:05.000000"
      }
    ]
  }
}
```

### Managing Chat History

**Clear Channel History** (Admin only):
```
!clearchat
```

This removes all chat history for the current channel.

---

## 4. Discord Bot Commands

### New Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!chat [character]: <message>` | Chat with character context tracking | Everyone |
| `!clearchat` | Clear chat history for current channel | Admin |

### Existing Commands (Still Available)

| Command | Description | Permission |
|---------|-------------|------------|
| `!settoken <token>` | Set Discord bot token | Admin |
| `!setopenai <url> <key>` | Configure OpenAI API | Admin |
| `!addcharacter <name> <display> <desc>` | Add AI character | Admin |
| `!characters` | List all AI characters | Everyone |
| `!manualsend <server> <channel> <char> <msg>` | Send manual message | Admin |
| `!ask [character] <message>` | Ask AI a question | Everyone |

---

## 5. Integration with Existing Features

### How Presets Work with Characters

When using presets with characters:
1. Preset blocks are sent first (if active preset exists)
2. Character description is added as a system message (if no system message in preset)
3. Chat history is added (if using `!chat`)
4. User message is sent last

### Message Flow Example

With an active preset and using `!chat`:

```
1. Preset Block 1 (role: system) - "You are a fantasy RPG narrator"
2. Preset Block 2 (role: system) - "Use vivid descriptions"
3. Character System Prompt - "You are the Dungeon Master"
4. Chat History (last 20 messages)
5. Current User Message
```

---

## 6. Best Practices

### For Presets

1. **Start Simple** - Begin with basic system messages, add complexity as needed
2. **Test Thoroughly** - Try different parameter combinations
3. **Name Clearly** - Use descriptive preset names
4. **Use Blocks Wisely** - Each block should have a specific purpose
5. **Toggle Strategically** - Use Active/Inactive to quickly test variations

### For User Characters

1. **Consistent Naming** - Use clear, memorable character IDs
2. **Rich Descriptions** - Help the AI understand character personality
3. **Unique Names** - Avoid conflicts with AI character names

### For Chat

1. **Clear Context** - Start new topics with `!clearchat` for fresh context
2. **Character Consistency** - Use the same character ID throughout a conversation
3. **Natural Flow** - Let conversations develop organically

### For AI Configuration

- **Temperature**:
  - Low (0.1-0.5): Focused, deterministic responses
  - Medium (0.6-1.0): Balanced creativity and coherence
  - High (1.1-2.0): More creative and varied, less predictable

- **Top P**:
  - Use with temperature for fine control
  - Lower values (0.1-0.5) = more focused
  - Higher values (0.6-1.0) = more diverse

- **Penalties**:
  - Presence Penalty: Encourages new topics
  - Frequency Penalty: Reduces word repetition
  - Start with low values (0.1-0.3) and adjust

---

## 7. Troubleshooting

### Preset Issues

**Q: My preset isn't being used**
- Check that it's set as active using "Set as Active"
- Verify the preset name matches exactly

**Q: Blocks aren't working**
- Ensure blocks are marked as "Active"
- Check that content is not empty

### Chat Issues

**Q: Chat history not showing in responses**
- Verify messages are using `!chat` command
- Check that channel history isn't full (clears after many messages)

**Q: Character not recognized**
- Ensure character name matches exactly (case-insensitive)
- Verify character exists in User Characters list

### AI Configuration Issues

**Q: Getting errors with penalties**
- Some AI providers (like Google AI) don't support penalties
- Disable penalty toggles when using incompatible providers

**Q: Max tokens exceeded**
- Reduce max_tokens value
- Maximum is 2,000,000 but provider may have lower limits

---

## 8. Example Scenarios

### Scenario 1: Role-Playing Game

**Setup:**
1. Create User Characters for each player (Alice, Bob, Charlie)
2. Create AI Character "DungeonMaster" with RPG system prompt
3. Create Preset "fantasy_rpg" with:
   - System message: "You are a Dungeon Master for a fantasy RPG"
   - Higher temperature (1.2) for creativity
   - Active reasoning for complex scenarios

**Usage:**
```
!chat Alice: "I search the room for treasure" looking under furniture
[Bot responds as DM]
!chat Bob: "I'll guard the door" draws sword and stands watch
[Bot responds considering both actions]
```

### Scenario 2: Creative Writing Workshop

**Setup:**
1. Create Preset "creative_writing" with:
   - Multiple system messages for different writing aspects
   - High temperature (1.3)
   - Presence penalty to encourage topic diversity

**Usage:**
```
!chat "Can you help me brainstorm ideas for a sci-fi story?"
[Bot provides creative suggestions]
!chat "Let's develop the main character"
[Bot builds on previous context]
```

### Scenario 3: Technical Support

**Setup:**
1. Create Preset "tech_support" with:
   - System message: "You are a technical support expert"
   - Low temperature (0.3) for precise answers
   - Example user/assistant blocks showing desired format

**Usage:**
```
!chat "My computer won't start, what should I check?"
[Bot provides systematic troubleshooting steps]
```

---

## 9. Advanced Features

### Dynamic Preset Switching

While there's currently one active preset at a time, you can:
1. Save multiple presets for different scenarios
2. Load and activate different presets as needed via GUI
3. Each preset maintains its own configuration

### Chat History Management

Chat history is automatically:
- Saved to config.json after each message
- Limited to last 20 messages for context
- Separated by channel ID (no cross-contamination)

### Multi-Block Conversation Design

Use multiple blocks to create complex conversation patterns:

```json
{
  "blocks": [
    {"active": true, "role": "system", "content": "You are a helpful assistant"},
    {"active": true, "role": "user", "content": "What's the weather like?"},
    {"active": true, "role": "assistant", "content": "I don't have access to real-time weather data, but I can help you find weather information."},
    {"active": true, "role": "system", "content": "Always be honest about limitations"}
  ]
}
```

This teaches the AI the desired interaction pattern.

---

## 10. Configuration File Reference

### Complete Structure

```json
{
  "discord": {
    "token": "YOUR_BOT_TOKEN"
  },
  "openai": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "YOUR_API_KEY"
  },
  "characters": [
    {
      "name": "assistant",
      "display_name": "Assistant",
      "description": "You are a helpful assistant.",
      "avatar_url": "",
      "avatar_file": ""
    }
  ],
  "user_characters": [
    {
      "name": "alice",
      "display_name": "Alice",
      "description": "A brave adventurer",
      "avatar_url": "",
      "avatar_file": "character_avatars/user_alice.png"
    }
  ],
  "presets": [
    {
      "name": "default",
      "ai_config": {
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
      },
      "blocks": [
        {
          "active": true,
          "role": "system",
          "content": "You are a helpful assistant."
        }
      ]
    }
  ],
  "active_preset": "default",
  "chat_history": {
    "123456789": []
  }
}
```

---

## Support

For issues or questions:
1. Check this documentation
2. Review the existing character and preset examples
3. Test with simple configurations first
4. Ensure all dependencies are installed (`pip install -r requirements.txt`)

---

**Version:** 2.0  
**Last Updated:** October 2025
