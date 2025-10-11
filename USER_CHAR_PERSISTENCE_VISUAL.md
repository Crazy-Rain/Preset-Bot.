# User Character Persistence - Quick Visual Guide

## What Changed

### Before This Update
```
User: !chat Alice Hello there!
      ↓
System: Uses Alice for THIS message only

User: !chat What's the weather?
      ↓
System: No character context (forgot Alice)

User: !chat Alice Tell me about yourself
      ↓
System: Uses Alice again (had to re-specify)
```

### After This Update
```
User: !chat Alice Hello there!
      ↓
System: Uses Alice
System: STORES "Alice" as user's active character in this channel

User: !chat What's the weather?
      ↓
System: LOOKS UP user's last character in channel
System: FINDS "Alice" from history
System: Uses Alice (automatic!)

User: !chat Tell me about yourself
      ↓
System: STILL finds "Alice" from history
System: Uses Alice (still automatic!)
```

## How It Works

### Character Lookup Flow

```
┌─────────────────────────────────────────────────┐
│ User sends: !chat message (no character name)  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ Was character specified in command?             │
└─────┬─────────────────────────────────┬─────────┘
      │ YES                               │ NO
      ▼                                   ▼
┌─────────────────┐         ┌────────────────────────────┐
│ Use specified   │         │ Look in channel history    │
│ character       │         │ (last 20 messages)         │
└─────────────────┘         └────────────┬───────────────┘
                                         │
                            ┌────────────▼───────────────┐
                            │ Find user's last message   │
                            │ with user_character set    │
                            └────────────┬───────────────┘
                                         │
                            ┌────────────▼───────────────┐
                            │ Found character?           │
                            └─┬──────────────────────┬───┘
                              │ YES                  │ NO
                              ▼                      ▼
                    ┌─────────────────┐    ┌────────────────┐
                    │ Use that        │    │ Proceed without│
                    │ character       │    │ character      │
                    └─────────────────┘    └────────────────┘
```

### Storage in Chat History

Each message now stores which character was active:

```json
{
  "chat_history": {
    "channel_123": [
      {
        "author": "user_456",
        "author_name": "JohnDoe",
        "user_character": "alice",     ← Stored here!
        "content": "Hello there!",
        "type": "user"
      },
      {
        "content": "Hi! How can I help?",
        "type": "assistant"
      },
      {
        "author": "user_456",
        "author_name": "JohnDoe",
        "user_character": "alice",     ← Auto-inherited from history!
        "content": "What's the weather?",
        "type": "user"
      }
    ]
  }
}
```

## User Scenarios

### Scenario 1: Single User, One Character

```
Channel: #general
User: JohnDoe

JohnDoe: !chat Alice Hello!
         [Alice stored for JohnDoe in #general]
         
JohnDoe: !chat How are you?
         [System finds Alice from history]
         [Alice used automatically]
         
JohnDoe: !chat Tell me a story
         [Alice still active]
```

### Scenario 2: Single User, Switching Characters

```
Channel: #roleplay
User: JohnDoe

JohnDoe: !chat Alice Greetings!
         [Alice active]
         
JohnDoe: !chat Bob Hello there!
         [Bob now active, Alice forgotten]
         
JohnDoe: !chat What's up?
         [Bob still active]
```

### Scenario 3: Multiple Users, Same Channel

```
Channel: #game
Users: Alice_Player, Bob_Player

Alice_Player: !chat Alice Hello everyone!
              [Alice stored for Alice_Player]
              
Bob_Player: !chat Bob Greetings!
            [Bob stored for Bob_Player]
            
Alice_Player: !chat What do you think?
              [System finds Alice for Alice_Player]
              
Bob_Player: !chat I agree!
            [System finds Bob for Bob_Player]
            
Each user maintains their own character!
```

### Scenario 4: Multiple Channels

```
User: JohnDoe

In #channel1:
JohnDoe: !chat Alice Hello
         [Alice active in #channel1]

In #channel2:
JohnDoe: !chat Bob Hi there
         [Bob active in #channel2]

Back in #channel1:
JohnDoe: !chat What's up?
         [Alice still active here]

Back in #channel2:
JohnDoe: !chat How goes it?
         [Bob still active here]

Characters are channel-specific!
```

## Code Changes

### bot.py - Modified chat command

```python
# OLD CODE (before):
if user_character:
    user_char = get_user_character_by_name(user_character)
    user_char_info = build_char_info(user_char)

# NEW CODE (after):
active_user_character = user_character

# If no character specified, look in channel history
if not active_user_character:
    chat_history = get_chat_history(channel_id)
    for msg in reversed(chat_history[-20:]):
        if msg.get("user_character") and msg.get("author") == current_user_id:
            active_user_character = msg.get("user_character")
            break

# Now use active_user_character
if active_user_character:
    user_char = get_user_character_by_name(active_user_character)
    user_char_info = build_char_info(user_char)
```

## Benefits

| Feature | Benefit |
|---------|---------|
| **Auto-Persistence** | Don't type character name every time |
| **User-Specific** | Each user has their own character |
| **Channel-Specific** | Different channels = different characters |
| **Easy Switching** | Just specify new character name |
| **Natural Flow** | More immersive roleplay experience |

## Commands

### Set/Change Character
```
!chat CharacterName message
```

### Use Persisted Character
```
!chat message
```

### Clear History (Resets Character)
```
!clearchat
```

## Technical Details

- **Lookup Depth**: Last 20 messages per channel
- **Matching**: By author ID (not username)
- **Storage**: In config.json's chat_history
- **Scope**: Per-channel, per-user
- **Performance**: O(n) where n ≤ 20 (fast)

## Example Session

```
=== Session Start ===

[10:00] User: !chat Alice: "Hello everyone!" waves
        System: ✓ Alice active for User in this channel
        Bot: "Greetings! I see you've arrived, Alice!"

[10:01] User: !chat: "How's the weather today?"
        System: ✓ Found Alice from history
        Bot: "The weather is fine, Alice! Perfect for an adventure."

[10:02] User: !chat What should I do first?
        System: ✓ Alice still active
        Bot: "As a brave warrior, you might want to check the armory first!"

[10:05] User: !chat Bob: "I'm here too!" 
        System: ✓ Switched to Bob
        Bot: "Welcome, Bob! Good to see you."

[10:06] User: !chat What's happening?
        System: ✓ Found Bob from history (most recent)
        Bot: "Things are going well, Bob!"

=== Session End ===

Character progression: Alice → Alice → Alice → Bob → Bob
Only needed to specify character twice!
```

## Comparison

| Aspect | Old Behavior | New Behavior |
|--------|--------------|--------------|
| **Character Spec** | Every message | Once per switch |
| **Memory** | None | Per-channel, per-user |
| **Typing** | Repetitive | Minimal |
| **Experience** | Fragmented | Seamless |
| **Setup** | None needed | None needed |

## Summary

User characters now persist automatically across messages in each channel on a per-user basis, creating a more natural and immersive roleplay experience without requiring constant re-specification of character names.
