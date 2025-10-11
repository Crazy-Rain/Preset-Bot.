# Avatar URL Validation Feature

## Overview

This feature adds comprehensive validation for avatar URLs when creating or updating characters in the Preset Bot GUI. It helps prevent issues where avatars don't show up in Discord due to invalid or inaccessible URLs.

## What's New

### 1. Avatar URL Validation Function
- Automatically checks avatar URLs for:
  - Valid URL format (must start with http:// or https://)
  - Accessibility (checks if the URL is reachable)
  - Image type validation (must be PNG, JPG, JPEG, GIF, or WEBP)
  - Image size checking (warns if > 2MB, rejects if > 8MB)

### 2. "Test URL" Button
- Added to both Characters and User Characters tabs
- Located next to the Avatar URL entry field
- Click to validate a URL before saving the character
- Provides immediate feedback on whether the URL will work

### 3. Automatic Validation on Save
- When adding or updating a character with an Avatar URL, the system automatically validates it
- Shows error dialog if the URL is invalid, with option to continue anyway
- Shows warning dialog for large images (but allows saving)

## How to Use

### Testing an Avatar URL

1. Open the GUI and navigate to the **Characters** or **User Characters** tab
2. Enter an Avatar URL in the "Avatar URL:" field
3. Click the **"Test URL"** button
4. Review the validation result:
   - ✓ **Success**: "Avatar URL is valid and accessible"
   - ⚠️ **Warning**: Image is large but usable
   - ❌ **Error**: Specific issue with the URL

### When Adding/Updating Characters

1. Fill in character details including Avatar URL
2. Click "Add Character" or "Update Selected"
3. If the URL has issues:
   - You'll see an error message explaining the problem
   - Choose whether to continue anyway or fix the URL
4. If the image is large:
   - You'll see a warning but can proceed

## Validation Messages

### Success Messages
- `✓ Avatar URL is valid and accessible` - URL works perfectly

### Warning Messages
- `⚠️ Image is large (X.XMB). Smaller images load faster in Discord` - Image works but is large

### Error Messages
- `URL is empty` - No URL provided
- `URL must start with http:// or https://` - Invalid URL format
- `URL returned HTTP 404 - image may not be accessible` - URL not found
- `Invalid image type. Must be PNG, JPG, GIF, or WEBP` - Wrong file type
- `Image is too large (X.XMB). Discord supports up to 8MB` - Image too big for Discord
- `Request timed out - URL may be slow or inaccessible` - Server not responding
- `Connection failed - check if URL is correct and accessible` - Can't reach server

## Common Issues and Solutions

### Issue: URL is behind authentication
**Solution**: Use a publicly accessible URL. Services like catbox.moe, imgur.com, or Discord's own CDN work well.

### Issue: URL returns 403 Forbidden
**Solution**: Some servers block direct hotlinking. Upload the image to an image hosting service instead.

### Issue: Image is too large
**Solution**: 
- Resize the image to 128x128 or 256x256 pixels
- Compress the image using online tools
- Upload to a service that automatically optimizes images

### Issue: Validation says URL is invalid but it works in browser
**Solution**: 
- The server might not support HEAD requests (validation tries this first)
- The URL might redirect multiple times
- Try clicking "continue anyway" if you're confident the URL is correct

## Technical Details

### What Gets Validated
1. **URL Format**: Checks if the URL starts with http:// or https://
2. **Accessibility**: Makes a HEAD request to check if the server responds with HTTP 200
3. **Content Type**: Verifies the Content-Type header indicates an image
4. **File Size**: Checks Content-Length header to ensure image isn't too large
5. **Fallback**: If HEAD request fails, tries a streaming GET request

### Timeouts
- Validation requests timeout after 10 seconds
- This prevents hanging on slow or unresponsive servers

### When Validation Runs
- **Manual**: When you click the "Test URL" button
- **Automatic**: When adding a character with an Avatar URL
- **Automatic**: When updating a character with a new/changed Avatar URL
- **Not Run**: When using the "Browse..." file upload option (files are uploaded to catbox.moe automatically)

## Best Practices

1. **Always test URLs** before saving characters
2. **Use image hosting services** designed for hotlinking (imgur, catbox.moe, Discord CDN)
3. **Keep images small** - 128x128 or 256x256 pixels is ideal
4. **Use PNG or JPG** for best compatibility
5. **Verify accessibility** - make sure the URL doesn't require login

## Benefits

✅ **Prevents broken avatars** - Catch issues before they affect Discord messages
✅ **Better user feedback** - Clear error messages explain exactly what's wrong
✅ **Saves time** - No need to debug why avatars aren't showing in Discord
✅ **Flexible** - Option to continue anyway if you know the URL is correct
✅ **Educational** - Learn what makes a good avatar URL
