# Configurable Chat History Limit

## Overview

The chat history limit determines how many previous messages are included in the AI's context when responding to messages in the `!chat` command. This allows you to customize the conversation memory based on your needs and the AI model's context window.

## Configuration

### Location
Settings → Configuration Tab → Chat History Settings

### Field
**Message History Limit**: A text box where you enter the number of messages to include

### Default Value
20 messages

## How It Works

When you use the `!chat` command, the bot includes previous messages from the conversation to give the AI context. The history limit determines how many recent messages are sent to the AI.

### Example with limit of 20 (default):
```
Channel has 50 messages
User: !chat What did we talk about?
→ AI receives last 20 messages as context
```

### Example with limit of 100:
```
Channel has 150 messages  
User: !chat What did we talk about?
→ AI receives last 100 messages as context
```

## Benefits of Higher Limits

### When to Increase
- **Long roleplay sessions**: Remember more of the story
- **Complex discussions**: Maintain context over extended conversations
- **Large context models**: If your AI model supports 32k, 100k, or more tokens

### Advantages
✅ AI remembers more of the conversation
✅ Better continuity in long roleplay sessions
✅ Can reference events from earlier in the discussion
✅ More coherent character development

### Example
```
Limit: 20 messages
- Can remember ~10 back-and-forth exchanges
- Good for short chats

Limit: 100 messages
- Can remember ~50 back-and-forth exchanges
- Good for extended roleplay sessions
```

## Benefits of Lower Limits

### When to Decrease
- **Limited model context**: If using models with small context windows (4k-8k tokens)
- **Cost optimization**: Fewer tokens used per request
- **Simple Q&A**: When long history isn't needed

### Advantages
✅ Uses fewer tokens (lower cost)
✅ Faster responses (less data to process)
✅ Fits in smaller context windows

## Token Usage Considerations

### How Messages Affect Tokens

Each message in history uses tokens:
- User message: ~10-100 tokens (depending on length)
- AI response: ~50-500 tokens (depending on length)

**Example calculation:**
- 20 messages × ~100 tokens average = ~2,000 tokens
- 100 messages × ~100 tokens average = ~10,000 tokens

### Model Context Windows

| Model Type | Context Window | Recommended Limit |
|------------|----------------|-------------------|
| GPT-3.5 | 4k tokens | 20-30 messages |
| GPT-4 | 8k tokens | 30-50 messages |
| GPT-4-32k | 32k tokens | 100-200 messages |
| Claude 2 | 100k tokens | 500+ messages |
| Llama 70B | Varies | Check your model |

## Setting the Limit

### Via GUI
1. Open the GUI
2. Go to **Configuration** tab
3. Find **Chat History Settings** section
4. Enter desired number in **Message History Limit** field
5. Click **Save Configuration**

### Valid Values
- **Minimum**: 1 message
- **Maximum**: No hard limit, but constrained by:
  - AI model's context window
  - Token costs
  - Response time

### Recommendations
- **Short chats**: 10-20 messages
- **Normal conversations**: 20-50 messages
- **Long roleplay**: 50-100 messages
- **Epic campaigns**: 100-200 messages (if model supports it)

## Impact on Features

### User Character Persistence
The history limit affects how far back the system looks for your last used character:

```
Limit: 20
- Searches last 20 messages for your character
- If you used character 25 messages ago, won't find it

Limit: 100
- Searches last 100 messages for your character
- More likely to find your character from earlier
```

### Context Quality
More messages = better context, but also:
- More tokens used
- Potentially slower responses
- May hit model limits

## Examples

### Example 1: Short Context (Limit: 10)
```
[Message 1-90: Not included]
[Message 91-100: Included in context]
User (Message 101): !chat What's happening?
→ AI sees messages 91-100
```

### Example 2: Medium Context (Limit: 50)
```
[Message 1-50: Not included]
[Message 51-100: Included in context]
User (Message 101): !chat What's happening?
→ AI sees messages 51-100
```

### Example 3: Long Context (Limit: 200)
```
[Message 1-50: Included in context]
[Message 51-250: Included in context]
User (Message 251): !chat What's happening?
→ AI sees all 250 messages (limited by history length)
```

## Best Practices

### 1. Match Your Model
```
Model with 4k context:  Limit = 20-30
Model with 8k context:  Limit = 30-60
Model with 32k context: Limit = 100-200
Model with 100k+ context: Limit = 500+
```

### 2. Consider Message Length
Long, detailed messages use more tokens:
- Detailed roleplay: Lower limit (messages are long)
- Quick chat: Higher limit (messages are short)

### 3. Monitor Performance
If you see:
- "Context too long" errors → Decrease limit
- AI forgetting recent events → Increase limit
- Slow responses → Decrease limit

### 4. Adjust for Use Case
```
Quick questions:        Limit = 10-20
Normal chat:           Limit = 20-50
Roleplay session:      Limit = 50-100
Epic campaign:         Limit = 100-200
```

## Technical Details

### Storage
- Setting stored in: `config.json`
- Field name: `"chat_history_limit"`
- Type: Integer
- Default: 20

### Code Location
- Configuration: `bot.py` → ConfigManager
- GUI: `gui.py` → Configuration tab
- Usage: `bot.py` → chat command

### Validation
- Minimum value: 1 (enforced)
- Invalid values: Defaults to 20
- String conversion: Automatic

## Troubleshooting

### Issue: "Context too long" error
**Solution**: Decrease the message history limit

### Issue: AI forgetting recent events
**Solution**: Increase the message history limit

### Issue: Slow responses
**Solution**: Decrease the limit (fewer tokens to process)

### Issue: High token costs
**Solution**: Decrease the limit (fewer tokens per request)

## Configuration File

The setting is stored in `config.json`:

```json
{
  "chat_history_limit": 20,
  "other_settings": "..."
}
```

You can also edit this file directly if needed.

## Summary

The configurable chat history limit gives you control over how much conversation context the AI receives. Adjust it based on:
- Your AI model's capabilities
- The type of conversations you're having
- Token cost considerations
- Response time preferences

Start with the default (20) and adjust based on your needs!
