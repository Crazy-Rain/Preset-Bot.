# Avatar Validation GUI Changes

## Characters Tab - Avatar Section

### Before
```
┌─ Avatar/Icon ────────────────────────────────────────────┐
│                                                           │
│  Avatar URL:  [_____________________________________]     │
│                                                           │
│                         --- OR ---                        │
│                                                           │
│  Avatar File: [____________________] [Browse...]          │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### After (New)
```
┌─ Avatar/Icon ────────────────────────────────────────────┐
│                                                           │
│  Avatar URL:  [_____________________________________] [Test URL]  ← NEW
│                                                           │
│                         --- OR ---                        │
│                                                           │
│  Avatar File: [____________________] [Browse...]          │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## User Characters Tab - Avatar Section

Same change applied to User Characters tab.

## Test URL Button Behavior

### When clicked with empty URL:
```
┌─────────────────────────────────────┐
│  Test Avatar URL              [i]   │
├─────────────────────────────────────┤
│                                     │
│  Please enter an Avatar URL to test │
│                                     │
│              [OK]                   │
└─────────────────────────────────────┘
```

### While testing:
```
┌─────────────────────────────────────┐
│  Testing Avatar URL                 │
├─────────────────────────────────────┤
│                                     │
│     Testing avatar URL...           │
│                                     │
└─────────────────────────────────────┘
```

### On success:
```
┌─────────────────────────────────────┐
│  Avatar URL Test              [i]   │
├─────────────────────────────────────┤
│                                     │
│  ✓ Avatar URL is valid and          │
│  accessible                         │
│                                     │
│              [OK]                   │
└─────────────────────────────────────┘
```

### On warning (large file):
```
┌─────────────────────────────────────┐
│  Avatar URL Test              [i]   │
├─────────────────────────────────────┤
│                                     │
│  ⚠️ Image is large (3.2MB).         │
│  Smaller images load faster in      │
│  Discord                            │
│                                     │
│              [OK]                   │
└─────────────────────────────────────┘
```

### On error:
```
┌─────────────────────────────────────┐
│  Avatar URL Test Failed       [X]   │
├─────────────────────────────────────┤
│                                     │
│  URL returned HTTP 404 - image may  │
│  not be accessible                  │
│                                     │
│              [OK]                   │
└─────────────────────────────────────┘
```

## Automatic Validation on Add/Update

### When adding character with invalid URL:
```
┌─────────────────────────────────────┐
│  Avatar URL Validation Failed  [?]  │
├─────────────────────────────────────┤
│                                     │
│  Invalid image type. Must be PNG,   │
│  JPG, GIF, or WEBP. Got: text/html  │
│                                     │
│  Do you want to continue anyway?    │
│                                     │
│           [Yes]    [No]             │
└─────────────────────────────────────┘
```

### When adding character with large image:
```
┌─────────────────────────────────────┐
│  Avatar URL Warning           [!]   │
├─────────────────────────────────────┤
│                                     │
│  ⚠️ Image is large (3.2MB).         │
│  Smaller images load faster in      │
│  Discord                            │
│                                     │
│              [OK]                   │
└─────────────────────────────────────┘
```

## Workflow Examples

### Example 1: Testing a URL before adding character

1. User enters avatar URL in field
2. User clicks "Test URL" button
3. System validates URL and shows result
4. If valid, user proceeds to add character
5. If invalid, user fixes URL or tries different one

### Example 2: Adding character with auto-validation

1. User fills in character details including avatar URL
2. User clicks "Add Character"
3. System automatically validates the avatar URL
4. If invalid, user is asked if they want to continue anyway
5. If they choose "No", they can fix the URL
6. If they choose "Yes", character is created anyway

### Example 3: Using file upload (bypasses validation)

1. User clicks "Browse..." button
2. User selects local image file
3. User clicks "Add Character"
4. System uploads file to catbox.moe (shows progress)
5. Character is created with the uploaded URL
6. No manual URL validation needed

## Benefits Visualization

```
Before:
User → Enter URL → Add Character → Avatar doesn't work in Discord → ?
                                                                     ↓
                                            User has to debug the issue

After:
User → Enter URL → Test URL → See validation result → Fix if needed → Add Character → Avatar works! ✓
       ↓
User → Browse file → Add Character → Auto-upload to catbox.moe → Avatar works! ✓
```

## Error Prevention Flow

```
                     ┌─────────────────┐
                     │  Enter Avatar   │
                     │      URL        │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Click Test URL │
                     │    (optional)   │
                     └────────┬────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         ┌────▼─────┐                   ┌────▼─────┐
         │  Valid   │                   │  Invalid │
         └────┬─────┘                   └────┬─────┘
              │                               │
              │                          ┌────▼─────┐
              │                          │ Fix URL  │
              │                          └────┬─────┘
              │                               │
              └───────────────┬───────────────┘
                              │
                     ┌────────▼────────┐
                     │  Add Character  │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │ Auto-validation │
                     │  (if URL only)  │
                     └────────┬────────┘
              ┌───────────────┴───────────────┐
              │                               │
         ┌────▼─────┐                   ┌────▼─────┐
         │  Valid   │                   │  Invalid │
         │  ✓ Save  │                   │ Show Dlg │
         └──────────┘                   └────┬─────┘
                                             │
                                  ┌──────────┴──────────┐
                                  │                     │
                            ┌─────▼──────┐        ┌────▼────┐
                            │ Continue   │        │  Cancel │
                            │ Anyway     │        │  & Fix  │
                            │  ✓ Save    │        └─────────┘
                            └────────────┘
```
