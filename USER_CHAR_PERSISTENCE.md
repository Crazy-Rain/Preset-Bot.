# User Character Persistence Feature

## Overview

The chat system now automatically remembers which user character you're playing as in each channel, so you don't need to specify it every time.

## How It Works

### Before (Manual Specification Required)
```
User: !chat Alice Hello there!
AI: (responds knowing Alice)

User: !chat What's the weather?
AI: (responds without Alice context - forgot who you're playing as)

User: !chat Alice Tell me about yourself
AI: (responds knowing Alice again - had to re-specify)
```

### After (Automatic Persistence)
```
User: !chat Alice Hello there!
AI: (responds knowing Alice)

User: !chat What's the weather?
AI: (STILL responds knowing you're Alice - remembers!)

User: !chat Tell me about yourself
AI: (STILL responds knowing you're Alice - no need to re-specify!)
```

## Key Features

### 1. Channel-Specific Memory
- Each channel remembers the last user character used **by each user**
- Different users in the same channel can play different characters
- Character persists until you switch to a different one

### 2. User-Specific
- The system looks for **your** last used character (by author ID)
- Other users' character choices don't affect yours
- Each user maintains their own character context in the channel

### 3. Automatic Inheritance
- When you use `!chat message` without specifying a character
- System checks your last 20 messages in that channel
- Finds the most recent user character you used
- Automatically applies that character's context

### 4. Easy Switching
- To change characters: `!chat NewCharacter message`
- To stop using a character: Clear the channel's chat history with `!clearchat`

## Usage Examples

### Example 1: Continuous Roleplay
```
User: !chat Alice: "Hello!" waves cheerfully
AI: [Responds as if user is Alice, a brave warrior]

User: !chat: "How are you today?"
AI: [STILL responds knowing you're Alice - no need to repeat]

User: !chat What weapons should I use?
AI: [STILL treats you as Alice, remembers you're a warrior]
```

### Example 2: Switching Characters
```
User: !chat Alice Hello!
AI: [Responds knowing you're Alice]

User: !chat Bob Greetings
AI: [Now responds knowing you're Bob - switched characters]

User: !chat How's it going?
AI: [STILL treats you as Bob - remembers the switch]
```

### Example 3: Multiple Users
```
User1: !chat Alice Hello!
AI: [Knows User1 is Alice]

User2: !chat Bob Hi there!
AI: [Knows User2 is Bob]

User1: !chat What's up?
AI: [Still knows User1 is Alice, even though User2 used Bob]
```

## Technical Implementation

### Character Lookup Logic
```python
# 1. Check if character specified in current command
if user_character:
    use character from command
else:
    # 2. Look in recent channel history (last 20 messages)
    for message in reversed(history):
        if message.author == current_user and message.user_character:
            use that character
            break
```

### Storage
- User character is stored in each chat message
- Field: `user_character` (string, character name or None)
- Persisted in config.json's `chat_history` section
- Organized by channel ID

### Context Inclusion
- Active user character's description is added to AI's system prompt
- Persists throughout the conversation
- Maintains consistent roleplay experience

## Benefits

✅ **Convenience** - Don't need to type character name every message
✅ **Natural Roleplay** - More immersive conversation flow
✅ **User Privacy** - Each user's character is independent
✅ **Channel Isolation** - Different channels can have different characters
✅ **Flexibility** - Can still switch characters anytime

## Command Reference

### Basic Usage
```
!chat message                    # Uses your last character in this channel
!chat CharacterName message      # Switches to CharacterName
```

### Managing Characters
```
!clearchat                       # Clears history (resets character memory)
```

### Character Setup
```
Create user characters in the GUI under "User Characters" tab
```

## Persistence Rules

1. **Per Channel**: Character memory is channel-specific
2. **Per User**: Each user has their own character in each channel
3. **Last 20 Messages**: Looks back up to 20 messages to find character
4. **Explicit Override**: Specifying a character always takes precedence
5. **No Fallback**: If no character found in history, proceeds without user character info

## Example Workflow

### First Time in Channel
```
User: !chat Alice: "Greetings!" smiles
→ System stores: Alice is your character in this channel
→ AI knows you're Alice

User: !chat: "Nice to meet you!"
→ System finds: Alice from previous message
→ AI still knows you're Alice
```

### Switching Characters Mid-Conversation
```
User: !chat Alice Hello
→ Alice active

User: !chat Bob Hi there
→ Bob now active (Alice forgotten)

User: !chat How are you?
→ Still Bob (last character specified)
```

### After Channel Clear
```
User: !clearchat
→ Chat history cleared

User: !chat Hello
→ No character active (history empty)

User: !chat Alice Hi
→ Alice now active again
```

## Comparison with Previous Behavior

| Aspect | Before | After |
|--------|--------|-------|
| **Character Specification** | Required every message | Required once, then remembered |
| **Scope** | Message-level | Channel & user-level |
| **Persistence** | None | Until switched or cleared |
| **User Isolation** | N/A | Each user independent |
| **Switching** | Just specify new one | Same - specify new one |

## Technical Notes

- Character lookup scans last 20 messages (configurable in code)
- Uses author ID for user matching (not username)
- Character info added to system prompt (persistent context)
- Backward compatible - explicit character spec still works
- No performance impact - simple list traversal

## Testing

Test file: `test_user_char_persistence.py`

```python
def test_user_character_persistence():
    # Add message with character "alice"
    add_chat_message(channel_id, {
        "author": user_id,
        "user_character": "alice",
        ...
    })
    
    # Look for last character in history
    for msg in reversed(history):
        if msg.author == user_id and msg.user_character:
            active = msg.user_character  # Found "alice"!
            break
    
    # Verify alice is found
    assert active == "alice"
```

Result: ✅ Test passed!

## Summary

User characters now persist in each channel, eliminating the need to re-specify them in every message. This creates a more natural roleplay experience while maintaining proper user isolation and channel boundaries.
