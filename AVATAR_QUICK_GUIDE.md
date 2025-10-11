# Avatar Display - Quick Visual Guide

## How to Set Up Avatars in the GUI

### Method 1: Using a URL (Recommended) ✅

**Steps:**
1. Go to "Characters" tab
2. Select or create a character
3. **Option A**: Paste a URL directly into "Avatar URL" field
4. **Option B**: Upload to Catbox
   - Click "Browse..." next to "Avatar File"
   - Select your local image
   - Click "Upload to Catbox"
   - URL is automatically filled in

**Result in Discord:**
```
┌────────────────────────────────────────┐
│  🖼️  Character Name          [Time]   │
│       Your message text here...        │
│                                         │
└────────────────────────────────────────┘
  ↑
  Avatar icon appears here (left of name)
```

### Method 2: Using Local File Only (Fallback)

**Steps:**
1. Go to "Characters" tab
2. Select or create a character
3. Click "Browse..." next to "Avatar File"
4. Select your local image
5. Leave "Avatar URL" empty

**Result in Discord:**
```
┌────────────────────────────────────────┐
│  [?]  Character Name          [Time]   │
│       Your message text here...        │
│                                         │
│  📎 avatar.png                         │
│  [Image preview shown inline]          │
└────────────────────────────────────────┘
  ↑
  Default icon (no custom avatar)
  But image is attached below message
```

### Method 3: Both URL and File

**Steps:**
1. Set both "Avatar URL" and "Avatar File"

**Result in Discord:**
```
┌────────────────────────────────────────┐
│  🖼️  Character Name          [Time]   │
│       Your message text here...        │
│                                         │
│  📎 avatar.png                         │
│  [Image preview shown inline]          │
└────────────────────────────────────────┘
  ↑
  Avatar icon appears (from URL)
  AND image attached (from file)
```

## Why Use Catbox?

The GUI includes built-in Catbox.moe integration:

✅ **Advantages:**
- Free image hosting
- No account required
- Permanent links
- Works with Discord webhooks
- Built right into the GUI

**How to use:**
1. Load your local image file
2. Click "Upload to Catbox" button
3. Wait for upload (shows progress)
4. URL automatically fills in
5. Done! Avatar will work in Discord

## Testing Your Setup

### Quick Test via GUI:
1. Go to "Manual Send" tab
2. Enter a Server ID and Channel ID
3. Select your character
4. Type a test message
5. Click "Send Message"
6. Check Discord to see the avatar

### Check the Console:
The "Console" tab will show:
- Whether upload to Catbox succeeded
- Message send confirmation
- Any errors with avatar loading

## Common Issues

### ❌ Avatar not showing as icon:
**Problem:** Only set local file, no URL
**Solution:** Use "Upload to Catbox" to get a URL

### ❌ "Upload to Catbox" fails:
**Problem:** Network issue or file too large
**Solution:** 
- Check internet connection
- Try smaller image (< 20MB)
- Use direct URL from imgur/other host

### ❌ Image shows twice:
**Problem:** Both URL and local file are set
**Solution:** This is normal if intentional. Remove local file if you don't want attachment.

## File Format Support

**Supported image formats:**
- PNG (recommended)
- JPG/JPEG
- GIF (static or animated)
- WEBP

**Recommended specs:**
- Size: 256x256 to 512x512 pixels
- Format: PNG for best quality
- File size: < 5MB (Discord limit for free)

## Example Workflow

```
1. Create character "Dashie"
2. Browse for local file: /home/user/avatars/dashie.png
3. Click "Upload to Catbox"
4. URL fills in: https://files.catbox.moe/abc123.png
5. Save character
6. Test in Manual Send tab
7. ✓ Avatar appears in Discord!
```

## Technical Note

**Why avatars need URLs:**
Discord's webhook API requires `avatar_url` to be a publicly accessible http/https URL. Local file paths (like `/home/user/image.png` or `C:\Users\...`) cannot be used for the webhook avatar icon because Discord servers cannot access your computer's files.

**The workaround:**
- Upload to a hosting service (Catbox, imgur, etc.)
- Get a public URL
- Use that URL in the avatar_url field

**Or:**
- Use local file only
- Image will be attached to messages instead of showing as icon
- Not as visually clean, but works without hosting
