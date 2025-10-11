# Message Splitting for Long Responses

## Overview

The webhook sending functionality now automatically handles long messages by splitting them into multiple messages when they exceed Discord's 2000 character limit.

## How It Works

### Short Messages (≤ 2000 characters)
Messages under Discord's limit are sent as a single message, just like before:
- **With avatar file**: Image attached to the message
- **With avatar URL**: URL used for webhook icon
- **Both**: URL for icon + image attached

### Long Messages (> 2000 characters)
Messages exceeding 2000 characters are automatically split into chunks:

1. **First message** (~1900 chars):
   - Contains the avatar image (if local file exists)
   - Contains the first chunk of text
   - Uses avatar URL for icon (if available)

2. **Subsequent messages** (~1900 chars each):
   - Contain remaining text chunks
   - Use avatar URL for icon (if available)
   - No image attachment (already sent in first message)

## Examples

### Example 1: Local Avatar File with Long Response

**Setup:**
- Avatar checkbox: Unchecked (local-only mode)
- Response length: 5000 characters

**Result:**
```
Message 1: [Image attached] + "First 1900 characters of response..."
Message 2: "Next 1900 characters of response..."
Message 3: "Remaining 1200 characters of response"
```

### Example 2: Avatar URL with Long Response

**Setup:**
- Avatar checkbox: Checked (uploaded to catbox.moe)
- Response length: 4500 characters

**Result:**
```
Message 1: [Avatar icon shown] + "First 1900 characters..."
Message 2: [Avatar icon shown] + "Next 1900 characters..."
Message 3: [Avatar icon shown] + "Remaining 700 characters"
```

### Example 3: Both Avatar URL and Local File with Long Response

**Setup:**
- Avatar checkbox: Checked
- Local backup exists
- Response length: 3900 characters

**Result:**
```
Message 1: [Avatar icon + image attached] + "First 1900 characters..."
Message 2: [Avatar icon shown] + "Remaining 2000 characters"
```

## Technical Details

### Chunk Size
- Messages are split at **1900 characters** per chunk
- This leaves a 100-character safety margin below Discord's 2000-character limit

### Avatar Handling in Split Messages
- **Avatar image file**: Only attached to the first message (prevents duplicate images)
- **Avatar URL**: Used in all messages for consistent webhook icon

### Benefits

✅ **No message loss** - Long AI responses are fully delivered  
✅ **Avatar sent first** - Image appears before text chunks  
✅ **Consistent branding** - Avatar icon maintained across all chunks (if URL exists)  
✅ **Automatic** - No user intervention required  
✅ **Efficient** - Image only sent once in first message  

## Code Implementation

The splitting logic is implemented in both:
- `bot.py` - `send_via_webhook()` method (line 1203)
- `gui.py` - `send_via_webhook()` method (line 776)

Both implementations are identical to ensure consistent behavior whether messages are sent via bot commands or the GUI.
