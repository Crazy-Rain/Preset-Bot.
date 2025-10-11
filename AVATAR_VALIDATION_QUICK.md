# Avatar URL Validation - Quick Reference

## Quick Start

### Test a URL Before Saving
1. Enter URL in "Avatar URL:" field
2. Click **"Test URL"** button
3. Review result message

### Fix Common Issues

| Issue | Solution |
|-------|----------|
| "URL must start with http://" | Add `https://` to the beginning of your URL |
| "HTTP 404 - image may not be accessible" | Check the URL is correct and the image exists |
| "Invalid image type" | Use PNG, JPG, GIF, or WEBP format only |
| "Image is too large" | Resize image to under 8MB (preferably under 2MB) |
| "Request timed out" | Try a different image host or check your internet |

## Validation Checklist

When entering an avatar URL, make sure:
- [ ] URL starts with `https://` or `http://`
- [ ] Image is PNG, JPG, JPEG, GIF, or WEBP format
- [ ] Image is under 8MB (under 2MB recommended)
- [ ] URL is publicly accessible (no login required)
- [ ] Image is square (1:1 aspect ratio) for best results

## Recommended Image Hosts

✅ **Works well:**
- catbox.moe (used by built-in file upload)
- imgur.com
- Discord CDN (files.discord.com)
- GitHub raw URLs (raw.githubusercontent.com)

❌ **Often causes issues:**
- Google Drive (requires authentication)
- Dropbox (requires authentication)
- Private servers (may not be accessible)
- URLs that redirect to login pages

## File Upload vs URL

### Use File Upload when:
- You have a local image file
- You don't want to find a hosting service
- You want automatic upload (uses catbox.moe)

### Use URL when:
- Image is already hosted online
- You want to use a specific URL
- You need to update the image without re-uploading

## Examples

### Good URLs
```
✓ https://i.imgur.com/abc123.png
✓ https://files.catbox.moe/xyz789.jpg
✓ https://cdn.discordapp.com/attachments/123/456/image.png
✓ https://raw.githubusercontent.com/user/repo/main/avatar.webp
```

### Bad URLs
```
✗ imgur.com/abc123                    (missing https://)
✗ https://example.com/image.html      (not an image)
✗ https://drive.google.com/file/...   (requires login)
✗ file:///C:/Users/me/image.png       (local file path)
```

## Troubleshooting

### Q: Validation says invalid but image works in browser?
**A:** Some servers don't support direct image access. Try:
1. Right-click image → "Copy Image Address"
2. Use that direct URL instead of the page URL
3. Or upload to an image hosting service

### Q: Can I use a URL from social media?
**A:** Usually not recommended because:
- May require authentication
- URLs might expire
- May have rate limiting
Better to download and re-upload to a dedicated image host

### Q: What if validation is wrong?
**A:** You can click "Yes" to continue anyway when prompted. The validation is a helper, not a hard block.

### Q: How do I make my image smaller?
**A:** Options:
1. Resize to 128x128 or 256x256 pixels
2. Use online compression tools (tinypng.com, etc.)
3. Convert to PNG or JPG with lower quality
4. Use built-in file upload (automatically optimized)

## Best Practices

1. 🎯 **Test first** - Always click "Test URL" before saving
2. 📏 **Keep it small** - 128x128 to 512x512 pixels is ideal
3. 🗜️ **Compress** - Keep file size under 1MB for fast loading
4. 🔒 **Use HTTPS** - More secure and required by some Discord servers
5. 🏠 **Reliable hosting** - Use established image hosting services
6. 📋 **Save URLs** - Keep a list of your avatar URLs for reuse

## Validation Response Times

| Check | Typical Time |
|-------|--------------|
| URL format | < 0.1 seconds |
| Accessibility | 0.5-2 seconds |
| Content type | 0.5-2 seconds |
| File size | 0.5-2 seconds |
| **Total** | **1-5 seconds** |

Timeout after 10 seconds if server is slow.
