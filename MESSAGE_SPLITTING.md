# Message Splitting for Long Responses

## Overview

The webhook sending functionality now automatically handles long messages by splitting them into multiple messages when they exceed Discord's 2000 character limit.

**NEW**: Messages are now split intelligently at sentence boundaries to avoid breaking sentences mid-way, providing a much better reading experience.

## How It Works

### Short Messages (≤ 2000 characters)
Messages under Discord's limit are sent as a single message, just like before:
- **With avatar file**: Image attached to the message
- **With avatar URL**: URL used for webhook icon
- **Both**: URL for icon + image attached

### Long Messages (> 2000 characters)
Messages exceeding 2000 characters are automatically split into chunks with **intelligent boundary detection**:

1. **Avatar image** (if exists):
   - Sent FIRST as a standalone message with empty text
   - Ensures the image appears before all text chunks
   
2. **First text chunk** (~1900 chars or less):
   - Split at sentence boundary when possible (. ! ? followed by space/newline)
   - Falls back to paragraph breaks (\n\n) if no sentence boundary nearby
   - Falls back to word boundaries (spaces) if no sentence/paragraph break
   - Uses avatar URL for icon (if available)

3. **Subsequent text chunks** (~1900 chars each):
   - Same intelligent splitting at boundaries
   - Use avatar URL for icon (if available)

## Intelligent Splitting

The new splitting algorithm prioritizes natural break points:

1. **Sentence boundaries** (highest priority): Splits after . ! ? followed by space/newline
2. **Paragraph breaks**: Splits at double newlines (\n\n)
3. **Word boundaries**: Splits at spaces to avoid breaking words
4. **Hard split**: Only as last resort if no other boundary found within range

This ensures:
- ✅ Sentences are never broken mid-way
- ✅ Paragraphs stay together when possible
- ✅ Words are never split
- ✅ Better readability for long responses

## Examples

### Example 1: Local Avatar File with Long Response

**Setup:**
- Avatar checkbox: Unchecked (local-only mode)
- Response length: 5000 characters with clear sentences

**Result:**
```
Message 1: [Image attached] (no text)
Message 2: "First ~1900 characters ending at sentence boundary."
Message 3: "Next ~1900 characters ending at sentence boundary."
Message 4: "Remaining characters"
```

### Example 2: Avatar URL with Long Response

**Setup:**
- Avatar checkbox: Checked (uploaded to catbox.moe)
- Response length: 4500 characters

**Result:**
```
Message 1: [Avatar icon shown] + "First ~1900 characters ending at sentence."
Message 2: [Avatar icon shown] + "Next ~1900 characters ending at sentence."
Message 3: [Avatar icon shown] + "Remaining ~700 characters"
```

### Example 3: Both Avatar URL and Local File with Long Response

**Setup:**
- Avatar checkbox: Checked
- Local backup exists
- Response length: 3900 characters

**Result:**
```
Message 1: [Avatar icon + image attached] (no text)
Message 2: [Avatar icon shown] + "First ~1900 characters ending at sentence."
Message 3: [Avatar icon shown] + "Remaining ~2000 characters"
```

## Technical Details

### Chunk Size
- Messages are split at **up to 1900 characters** per chunk
- This leaves a 100-character safety margin below Discord's 2000-character limit
- Actual chunk size may be smaller to respect sentence/paragraph boundaries

### Intelligent Boundary Detection
The splitting algorithm searches backwards from position 1900 to find the best split point:

1. **Sentence boundary** (within last 200 chars): `. ! ?` followed by space/newline
2. **Paragraph break** (within last 200 chars): Double newline `\n\n`
3. **Word boundary** (within last 100 chars): Any space character
4. **Hard split** (fallback): Splits at position 1900 if no boundaries found

### Avatar Handling in Split Messages
- **Avatar image file**: Sent FIRST as a separate message (no text, just image)
- **Avatar URL**: Used in all subsequent messages for consistent webhook icon
- This ensures the image appears before the text, as requested

### Benefits

✅ **No broken sentences** - Text always splits at natural boundaries  
✅ **Avatar sent first** - Image appears before all text chunks  
✅ **Consistent branding** - Avatar icon maintained across all chunks (if URL exists)  
✅ **Automatic** - No user intervention required  
✅ **Efficient** - Image only sent once in first message  
✅ **Better readability** - Respects sentence and paragraph structure  

## Code Implementation

The splitting logic is implemented in:
- `bot.py` - `split_text_intelligently()` function (shared utility)
- `bot.py` - `send_via_webhook()` method (line ~1350)
- `gui.py` - `send_via_webhook()` method (line ~820)

Both implementations use the same intelligent splitting function to ensure consistent behavior whether messages are sent via bot commands or the GUI.

## Config Reload Feature

**NEW**: The bot now automatically reloads configuration before executing commands that access character or lorebook data. This means:

✅ Changes made in the GUI are immediately available to bot commands  
✅ No need to restart the bot after updating characters, avatars, or lorebooks  
✅ `!chat`, `!ask`, and `!manualsend` commands always use fresh data  

Commands that auto-reload config:
- `!chat` - Reloads before accessing character/user character data
- `!ask` - Reloads before accessing character data
- `!manualsend` - Reloads before accessing character data

The ConfigManager now has a `reload_config()` method that can be called to refresh data from disk.
