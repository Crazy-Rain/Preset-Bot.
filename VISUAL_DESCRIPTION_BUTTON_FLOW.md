# Visual Guide: Description Button Avatar-First Behavior

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  User Types: !viewu alice                                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Bot Responds with Character Info Embed                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ User Character: Alice                                │  │
│  │ Character ID: alice                                  │  │
│  │ [Thumbnail shows avatar]                             │  │
│  │                                                       │  │
│  │ [Show Description] Button                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓
              User clicks [Show Description]
                          ↓
         ┌────────────────────────────────┐
         │ Does character have avatar?    │
         └────────────────────────────────┘
                 ↓                  ↓
               YES                 NO
                 ↓                  ↓
    ┌─────────────────────┐   ┌─────────────────────┐
    │ STEP 1:             │   │ STEP 1:             │
    │ Send Avatar Image   │   │ Send Description    │
    │ (interaction.       │   │ (interaction.       │
    │  response)          │   │  response)          │
    └─────────────────────┘   └─────────────────────┘
                 ↓
    ┌─────────────────────┐
    │ STEP 2:             │
    │ Send Description    │
    │ (interaction.       │
    │  followup)          │
    └─────────────────────┘
```

## Before vs After

### BEFORE (Old Behavior)
```
User clicks [Show Description]
         ↓
┌─────────────────────────────────┐
│ Description                     │
│ ─────────────────────────────── │
│ Alice is a brave warrior...     │
│ (with thumbnail in corner)      │
└─────────────────────────────────┘
```

### AFTER (New Behavior)
```
User clicks [Show Description]
         ↓
┌─────────────────────────────────┐
│ [Full Avatar Image]             │
│                                 │
│     [Alice's Portrait]          │
│                                 │
└─────────────────────────────────┘
         ↓ (immediately after)
┌─────────────────────────────────┐
│ Description                     │
│ ─────────────────────────────── │
│ Alice is a brave warrior from   │
│ the north. She wields...        │
└─────────────────────────────────┘
```

## Complete Example Flow

### Scenario: User Character with Avatar and Long Description

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: User Command                                       │
└─────────────────────────────────────────────────────────────┘
Discord: !viewu alice

┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Bot Shows Character Info                           │
└─────────────────────────────────────────────────────────────┘
Bot: ┌────────────────────────────────────────┐
     │ User Character: Alice the Brave       │ 
     │ Character ID: alice                   │
     │ 🖼️ [thumbnail]                        │
     │                                       │
     │ [Show Description] ← Button           │
     └────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  STEP 3: User Clicks Button                                 │
└─────────────────────────────────────────────────────────────┘
User: *clicks [Show Description]*

┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Bot Sends Avatar FIRST (New!)                      │
└─────────────────────────────────────────────────────────────┘
Bot: ┌────────────────────────────────────────┐
     │                                       │
     │      🖼️ [Full Avatar Image]          │
     │                                       │
     │    [Alice's character portrait]       │
     │                                       │
     └────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Bot Sends Description Part 1                       │
└─────────────────────────────────────────────────────────────┘
Bot: ┌────────────────────────────────────────┐
     │ Description (Part 1/2)                │
     │ ──────────────────────────────────── │
     │ Alice is a brave warrior from the    │
     │ northern kingdoms. She has trained   │
     │ her entire life in the art of...     │
     │ (continues for ~4000 characters)     │
     └────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Bot Sends Description Part 2                       │
└─────────────────────────────────────────────────────────────┘
Bot: ┌────────────────────────────────────────┐
     │ Description (Part 2/2)                │
     │ ──────────────────────────────────── │
     │ ...and now seeks to prove her worth  │
     │ by completing the ancient trial of   │
     │ champions.                           │
     └────────────────────────────────────────┘
```

## Side-by-Side Comparison

### !viewc (AI Character) vs !viewu (User Character)

Both commands now work the same way:

| Command | Avatar First? | Description After? | Scenario Button |
|---------|--------------|-------------------|-----------------|
| !viewc  | ✅ Yes       | ✅ Yes            | Unchanged       |
| !viewu  | ✅ Yes       | ✅ Yes            | N/A             |

## Technical Flow

```
show_description button clicked
         ↓
┌────────────────────────────────────────┐
│ Check if avatar exists                 │
│ (avatar_url OR avatar_file)            │
└────────────────────────────────────────┘
         ↓
    ┌────────┴────────┐
    ↓                 ↓
  Avatar            No Avatar
  Exists            
    ↓                 ↓
┌─────────────┐  ┌─────────────────────┐
│ Create      │  │ Skip to             │
│ avatar      │  │ description         │
│ embed       │  │ (no avatar msg)     │
└─────────────┘  └─────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ If avatar_url: embed.set_image(url)     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ If avatar_file: attach discord.File     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Send avatar embed                       │
│ (interaction.response.send_message)     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Send description text                   │
│ (interaction.followup.send)             │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ If description > 4096 chars:            │
│ Split and send multiple followups       │
└─────────────────────────────────────────┘
```

## Key Points

✅ **Avatar sent first** - Always appears before description text  
✅ **Full image display** - Uses `set_image()` for large display, not thumbnail  
✅ **Ephemeral messages** - Only visible to the user who clicked  
✅ **Smart splitting** - Long descriptions handled automatically  
✅ **Graceful fallback** - Works correctly without an avatar  
✅ **Consistent pattern** - Matches `send_via_webhook` behavior  

## User Experience

### What Users See

1. Click "Show Description" button
2. See full avatar image appear (if character has one)
3. See description text appear right after
4. If description is long, see it split across multiple messages

### Benefits

- **Better visual presentation**: Full avatar image instead of small thumbnail
- **Clearer organization**: Avatar and description are separate, distinct messages
- **Familiar pattern**: Works the same way as chat responses
- **No errors**: Handles long descriptions without breaking
