# Avatar Upload Workflow

## Before (Problem)
```
User selects local file → Character saved with avatar_file
                       → Webhook tries to use local path
                       → Avatar doesn't show (webhooks need URLs)
```

## After (Solution)
```
User selects local file → Automatic upload to catbox.moe
                       → Hosted URL returned (e.g., https://files.catbox.moe/abc123.png)
                       → Character saved with avatar_url
                       → Webhook uses URL
                       → Avatar shows correctly! ✓
```

## User Experience

### When adding a character with avatar:

1. **User action**: Browse and select avatar image
2. **User action**: Fill in character details
3. **User action**: Click "Add Character"
4. **System**: "Uploading avatar to catbox.moe..."
5. **System**: "Avatar uploaded successfully! URL: https://files.catbox.moe/..."
6. **Result**: Character saved with working avatar URL

### Benefits:
- ✓ Webhooks now work with avatars
- ✓ No manual URL entry needed
- ✓ Free, permanent hosting
- ✓ Real-time updates (no restart required)
- ✓ Local backup still saved

## Technical Details

- **Upload endpoint**: POST to https://catbox.moe/user/api.php
- **Timeout**: 30 seconds
- **Fallback**: If upload fails, character is still created (just without avatar URL)
- **Backup**: Local file always saved to character_avatars/ folder
