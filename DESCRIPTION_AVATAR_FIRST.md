# Description Button Avatar-First Feature

## Overview

The Description button in `!viewc` and `!viewu` commands now displays the character's avatar image first, followed by the description text. This matches the behavior of chat responses where avatars are sent before text.

## What Changed

### Before
When clicking "Show Description":
- Description text was sent immediately
- Avatar was only shown as a thumbnail in the character info embed

### After  
When clicking "Show Description":
1. **First Message**: Character's avatar image (if available)
2. **Subsequent Messages**: Description text

## Commands Affected

### !viewu - View User Character
The "Show Description" button now:
1. Sends the user character's avatar as a full image
2. Follows with the character description

### !viewc - View AI Character
The "Show Description" button now:
1. Sends the AI character's avatar as a full image  
2. Follows with the character description

**Note:** The "Show Scenario" button behavior is unchanged.

## How It Works

### With Avatar
```
User: !viewu alice
Bot: [Shows character info embed with thumbnail]
     [Show Description] button

User: *clicks Show Description*
Bot: [Message 1: Full avatar image]
     [Message 2: Description text]
     [Message 3: Description part 2 (if long)]
```

### Without Avatar
```
User: !viewu bob  
Bot: [Shows character info embed]
     [Show Description] button

User: *clicks Show Description*
Bot: [Message 1: Description text only]
```

## Benefits

✅ **Consistent with chat responses** - Matches the avatar-first pattern used in `!chat` and `!ask`  
✅ **Better visual presentation** - Full image display instead of small thumbnail  
✅ **Clear separation** - Avatar and description are distinct messages  
✅ **Graceful fallback** - Works correctly even without an avatar  

## Technical Details

### Avatar Sources
The feature works with both:
- **Avatar URLs** (`avatar_url` field)
- **Local avatar files** (`avatar_file` field)

### Message Types
All messages are sent as **ephemeral** (only visible to the user who clicked the button).

### Long Descriptions
If the description exceeds 4096 characters:
1. Avatar sent first
2. Description split into multiple parts
3. Each part sent as a separate followup message

## Example Scenarios

### Scenario 1: Short Description with Avatar
```
Step 1: Avatar image embed
Step 2: Description embed with full text
```

### Scenario 2: Long Description with Avatar
```
Step 1: Avatar image embed
Step 2: Description (Part 1/3) embed
Step 3: Description (Part 2/3) embed  
Step 4: Description (Part 3/3) embed
```

### Scenario 3: No Avatar
```
Step 1: Description embed (or Description Part 1/N if long)
Step 2: Description Part 2/N (if long)
...
```

## Related Features

This feature complements:
- **Avatar-first chat responses** (`send_via_webhook`)
- **Embed description splitting** (handles long descriptions)
- **Avatar management** (`!image` and `!cimage` commands)

## For Developers

### Code Changes
- `DescriptionView` class: Added `avatar_url` and `avatar_file` parameters
- `CharacterView` class: Added `avatar_url` and `avatar_file` parameters
- `show_description` button callback: Sends avatar first, then description

### Testing
See `test_description_avatar_first.py` for validation tests.
