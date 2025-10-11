# Avatar Display Fix for Discord Webhooks

## The Issue

Discord webhooks have limitations with how avatars can be displayed:

1. **`avatar_url` parameter**: Requires a publicly accessible URL (http/https)
   - ✅ Works: URLs from catbox.moe, imgur, Discord CDN, etc.
   - ❌ Doesn't work: Local file paths, file:// URLs

2. **Local avatar files**: Cannot be set as the webhook's avatar icon directly
   - Discord API doesn't support sending avatar bytes for per-message avatars
   - The `avatar_url` parameter only accepts URLs

## The Solution

The code has been updated to handle avatars in the following priority order:

### 1. Avatar URL (Preferred) ✅
If you set an `avatar_url` in the Characters tab:
- The webhook will display this image as the character's avatar icon
- This appears in the Discord user icon area (left side of message)
- **This is the recommended approach for character avatars**

### 2. Local Avatar File (Attached to Message) 🖼️
If you only set an `avatar_file` (local file):
- The image will be **attached to the message** as a file
- It appears in the message content area (below the text)
- The webhook won't have a custom avatar icon, but the image is still sent

### 3. Both URL and File
If both are set:
- The URL is used for the webhook avatar icon
- The local file is also attached to the message
- This gives you both the avatar icon AND the image in the message

### 4. No Avatar
If neither is set:
- The webhook uses Discord's default avatar
- No image is attached to the message

## Updated Code

Both `bot.py` and `gui.py` now have the same improved implementation:

```python
async def send_via_webhook(self, channel, content: str, character: dict) -> None:
    # Get avatar URL and file
    avatar_url = character.get("avatar_url", "")
    avatar_file = character.get("avatar_file", "")
    
    # Prepare local file as Discord attachment
    avatar_image = None
    if avatar_file and os.path.exists(avatar_file):
        avatar_image = discord.File(avatar_file, filename="avatar.png")
    
    # Send with appropriate parameters
    if avatar_url:
        # Use URL for webhook avatar icon
        if avatar_image:
            # Also attach the file
            await webhook.send(content=content, username=display_name, 
                             avatar_url=avatar_url, file=avatar_image)
        else:
            await webhook.send(content=content, username=display_name, 
                             avatar_url=avatar_url)
    elif avatar_image:
        # Only local file - attach to message
        await webhook.send(content=content, username=display_name, 
                         file=avatar_image)
    else:
        # No avatar
        await webhook.send(content=content, username=display_name)
```

## Recommendations

### For Best Results:
1. **Upload your avatar images** to a public hosting service:
   - Use catbox.moe (built-in upload in GUI)
   - Use imgur, Discord CDN, or similar
   - Copy the URL to the `avatar_url` field

2. **Use the "Upload to Catbox" button** in the Characters tab:
   - Select your local file
   - Click "Upload to Catbox"
   - URL is automatically set in the avatar_url field
   - This gives you the proper avatar icon in Discord

### Alternative (Local Files Only):
If you can't use URLs:
- Set only the `avatar_file` (local path)
- The image will appear attached to each message
- Won't show as the webhook's avatar icon
- This is a fallback option, not ideal for visual consistency

## Visual Comparison

### With avatar_url (Recommended):
```
┌─────────────────────────────────────┐
│ [Avatar]  Character Name            │
│ Icon     Message text here...       │
│                                      │
└─────────────────────────────────────┘
```

### With avatar_file only (Fallback):
```
┌─────────────────────────────────────┐
│ [Default] Character Name            │
│ Icon     Message text here...       │
│                                      │
│          [Attached: avatar.png]     │
│          [Image thumbnail shown]    │
└─────────────────────────────────────┘
```

## Testing the Fix

1. **Test with URL**:
   - Go to Characters tab
   - Upload an image to Catbox
   - Send a message
   - ✅ Avatar should appear as webhook icon

2. **Test with local file**:
   - Go to Characters tab
   - Set only avatar_file (browse for local file)
   - Clear avatar_url
   - Send a message
   - ✅ Image should be attached to message

3. **Test with both**:
   - Set both avatar_url and avatar_file
   - Send a message
   - ✅ Avatar icon + attached image both appear

## Technical Notes

- Discord webhook `avatar_url` parameter only accepts http/https URLs
- Per-message avatar customization requires a valid URL
- Local files cannot be used for the webhook avatar icon due to Discord API limitations
- Attaching files to messages is a workaround for local avatar files
- The `discord.File` class handles local file attachments properly

## Why This Matters

The original issue was that setting an avatar in the GUI didn't show up in Discord. This was because:

1. If you only set a local file path → Discord couldn't access it as a URL
2. The code wasn't using the avatar_url properly → Not passing it to webhook
3. The code wasn't attaching local files → Missing the fallback option

The fix ensures:
- ✅ URLs work properly for avatar icons
- ✅ Local files are attached as a fallback
- ✅ Both options can work together
- ✅ Clear guidance on best practices
