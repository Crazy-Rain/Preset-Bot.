# Avatar Preview Feature - Visual Guide

## GUI Layout with Avatar Preview

### Characters Tab - Before vs After

**BEFORE (Without Preview):**
```
┌─ Add/Edit Character ──────────────────────────────────────────────┐
│                                                                    │
│  Character Name (ID):  [tech_support___]  (lowercase, no spaces)  │
│  Display Name:         [Tech Support___]  (shown in Discord)      │
│  Description:          ┌─────────────────────────────────┐        │
│                        │ You are a tech support bot...   │        │
│                        └─────────────────────────────────┘        │
│  Scenario:             ┌─────────────────────────────────┐        │
│                        │ Default scenario...             │        │
│                        └─────────────────────────────────┘        │
│                                                                    │
│  ┌─ Avatar/Icon ─────────────────────────────────────────┐        │
│  │                                                        │        │
│  │  Avatar URL:  [https://example.com/avatar.png] [Test URL]      │
│  │                                                        │        │
│  │                    --- OR ---                          │        │
│  │                                                        │        │
│  │  Avatar File: [/path/to/file.png     ] [Browse...]    │        │
│  │                                                        │        │
│  └────────────────────────────────────────────────────────┘        │
│                                                                    │
│  [Add Character] [Update Selected] [Clear Form]                   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**AFTER (With Preview):**
```
┌─ Add/Edit Character ──────────────────────────────────────┬─ Avatar Preview ──┐
│                                                            │                   │
│  Character Name (ID):  [tech_support___]  (lowercase...)  │  ┌─────────────┐ │
│  Display Name:         [Tech Support___]  (shown in...)   │  │             │ │
│  Description:          ┌─────────────────────────────┐    │  │   [IMAGE]   │ │
│                        │ You are a tech support bot..│    │  │  128x128    │ │
│                        └─────────────────────────────┘    │  │             │ │
│  Scenario:             ┌─────────────────────────────┐    │  └─────────────┘ │
│                        │ Default scenario...         │    │                   │
│                        └─────────────────────────────┘    │  [Load Preview]   │
│                                                            │                   │
│  ┌─ Avatar/Icon ────────────────────────────────┐         │                   │
│  │                                               │         │                   │
│  │  Avatar URL:  [https://example.com/avatar.png] [Test URL]                  │
│  │                                               │         │                   │
│  │                    --- OR ---                 │         │                   │
│  │                                               │         │                   │
│  │  Avatar File: [/path/to/file.png  ] [Browse...]        │                   │
│  │                                               │         │                   │
│  └───────────────────────────────────────────────┘         │                   │
│                                                            │                   │
│  [Add Character] [Update Selected] [Clear Form]            │                   │
│                                                            │                   │
└────────────────────────────────────────────────────────────┴───────────────────┘
```

## How to Use Avatar Preview

### Step-by-Step Workflow

1. **Enter Avatar URL or Select File**
   ```
   Option A: Enter URL
   Avatar URL: https://i.imgur.com/example.png
   
   Option B: Browse for file
   Avatar File: /home/user/Pictures/avatar.png
   ```

2. **Click "Load Preview" Button**
   ```
   [Load Preview] ← Click this button
   ```

3. **View the Preview**
   ```
   ┌─ Avatar Preview ──┐
   │  ┌─────────────┐  │
   │  │   [IMAGE]   │  │  ← Your avatar appears here
   │  │  128x128    │  │     at Discord size
   │  └─────────────┘  │
   │  [Load Preview]   │
   └───────────────────┘
   ```

4. **Save Character**
   ```
   If preview looks good:
   [Add Character] ← Click to save
   
   If preview doesn't look good:
   - Adjust the avatar URL/file
   - Click "Load Preview" again
   - Repeat until satisfied
   ```

## Preview States

### No Avatar Loaded
```
┌─ Avatar Preview ──┐
│ ┌───────────────┐ │
│ │ No avatar     │ │
│ │ loaded        │ │
│ └───────────────┘ │
│ [Load Preview]    │
└───────────────────┘
```

### Loading...
```
┌─ Avatar Preview ──┐
│ ┌───────────────┐ │
│ │ Loading...    │ │
│ └───────────────┘ │
│ [Load Preview]    │
└───────────────────┘
```

### Success - Avatar Displayed
```
┌─ Avatar Preview ──┐
│ ┌───────────────┐ │
│ │    ╭─────╮    │ │
│ │    │ ^_^ │    │ │
│ │    ╰─────╯    │ │
│ └───────────────┘ │
│ [Load Preview]    │
└───────────────────┘
```

### Error - Failed to Load
```
Dialog appears:
┌─────────────────────────────┐
│  Preview Error         [X]  │
├─────────────────────────────┤
│                             │
│  Failed to load image from  │
│  URL (HTTP 404)             │
│                             │
│           [OK]              │
└─────────────────────────────┘
```

## Benefits

✅ **Visual Verification**
- See exactly how avatar will appear
- No need to save and test in Discord
- Instant visual feedback

✅ **Size Preview**
- Shows avatar at Discord's actual size (128x128)
- Catch issues with image scaling
- Ensure clarity at small size

✅ **Quick Iteration**
- Load, view, adjust, repeat
- Fast workflow for finding perfect avatar
- No commits to database until satisfied

✅ **Error Prevention**
- Catch broken URLs before saving
- See if image is too small/large
- Verify image quality

## Technical Details

### Image Processing
- Uses PIL/Pillow library
- Resizes to 128x128 with LANCZOS resampling (high quality)
- Maintains aspect ratio (creates thumbnail)
- Supports PNG, JPG, JPEG, GIF, WEBP

### Loading Sources
- **URL**: Downloads image via HTTP request
- **File**: Loads from local filesystem
- **Timeout**: 10 seconds for URL downloads
- **Cache**: Image stored in memory to prevent garbage collection

### Performance
- Preview loads on-demand (not automatic)
- Avoids unnecessary network requests
- Lightweight - only loads when button clicked
- No impact on GUI startup time

## Examples

### Example 1: Loading from URL
```
1. User enters: https://i.imgur.com/abc123.png
2. User clicks: [Load Preview]
3. System: Downloads image from URL
4. System: Resizes to 128x128
5. System: Displays in preview panel
6. User: Sees preview, looks good!
7. User: Clicks [Add Character]
```

### Example 2: Loading from File
```
1. User clicks: [Browse...]
2. User selects: /home/user/avatar.png
3. User clicks: [Load Preview]
4. System: Loads image from file
5. System: Resizes to 128x128
6. System: Displays in preview panel
7. User: Sees preview, looks good!
8. User: Clicks [Add Character]
```

### Example 3: Bad URL
```
1. User enters: https://broken.com/missing.png
2. User clicks: [Load Preview]
3. System: Attempts to download
4. System: Receives HTTP 404
5. Dialog: "Failed to load image from URL (HTTP 404)"
6. User: Fixes URL or tries different image
7. User: Clicks [Load Preview] again
```

## Comparison with Other Features

| Feature | Test URL | Load Preview |
|---------|----------|--------------|
| **Purpose** | Validate URL is accessible | Show visual preview |
| **Speed** | 1-5 seconds | 1-5 seconds |
| **Result** | Text message (valid/invalid) | Image display |
| **Use Case** | Check URL works | See how it looks |
| **When to Use** | Before loading preview | After entering URL/file |

**Recommended Workflow:**
1. Enter Avatar URL
2. Click "Test URL" (validates accessibility)
3. Click "Load Preview" (shows visual)
4. If both pass, save character

## User Characters Tab

The same preview feature is available in the User Characters tab with identical functionality:

```
┌─ Add/Edit User Character ─────────────────────────────┬─ Avatar Preview ──┐
│                                                        │                   │
│  Character Name (ID):  [alice________]  (lowercase...) │  ┌─────────────┐ │
│  Display Name:         [Alice________]  (shown in...)  │  │             │ │
│  Description:          ┌──────────────────────────┐    │  │   [IMAGE]   │ │
│                        │ Alice is a brave warrior │    │  │  128x128    │ │
│                        └──────────────────────────┘    │  │             │ │
│                                                        │  └─────────────┘ │
│  ┌─ Avatar/Icon ─────────────────────────────┐        │                   │
│  │                                            │        │  [Load Preview]   │
│  │  Avatar URL:  [https://...] [Test URL]    │        │                   │
│  │               --- OR ---                   │        │                   │
│  │  Avatar File: [...]        [Browse...]     │        │                   │
│  └────────────────────────────────────────────┘        │                   │
│                                                        │                   │
│  [Add User Character] [Update Selected] [Clear Form]   │                   │
│                                                        │                   │
└────────────────────────────────────────────────────────┴───────────────────┘
```

## Notes

- Preview panel appears in both Characters and User Characters tabs
- Preview is positioned to the right of the form (column 3)
- Uses available GUI space efficiently
- Does not interfere with existing controls
- Fully optional - you can still save without previewing
- Preview persists until form is cleared or new image loaded
