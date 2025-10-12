# Quick Reference: Description Button Update

## What Changed?

The **Show Description** button in `!viewc` and `!viewu` commands now sends the character's avatar image first, then the description text.

## Commands Affected

- `!viewu` - View User Character
- `!viewc` - View AI Character

## How It Works Now

### Before (Old)
```
Click [Show Description] → Description text appears
```

### After (New)
```
Click [Show Description] → Avatar image appears → Description text appears
```

## Quick Examples

### Example 1: User Character with Avatar
```
!viewu alice
[Click Show Description]
→ Message 1: Alice's avatar (full image)
→ Message 2: Alice's description text
```

### Example 2: AI Character with Long Description
```
!viewc gandalf
[Click Show Description]
→ Message 1: Gandalf's avatar (full image)
→ Message 2: Description (Part 1/3)
→ Message 3: Description (Part 2/3)
→ Message 4: Description (Part 3/3)
```

### Example 3: Character without Avatar
```
!viewu bob
[Click Show Description]
→ Message 1: Bob's description text
(No avatar shown since Bob doesn't have one)
```

## Key Points

✅ Avatar always appears **before** description  
✅ Avatar displays as **full image** (not thumbnail)  
✅ Works with both **URL** and **file** avatars  
✅ Handles **long descriptions** automatically  
✅ **Ephemeral messages** (only you can see them)  
✅ Characters **without avatars** still work fine  

## Why This Change?

This makes the Description button work the same way as chat responses (`!chat`, `!ask`), where avatars always appear before text. This provides a more consistent and visually appealing experience.

## Related Commands

- `!image <character> <url>` - Set AI character avatar
- `!cimage <character> <url>` - Set user character avatar
- `!viewc [character]` - View AI character
- `!viewu [character]` - View user character

## Need Help?

See full documentation:
- `DESCRIPTION_AVATAR_FIRST.md` - Complete feature guide
- `VISUAL_DESCRIPTION_BUTTON_FLOW.md` - Visual diagrams and examples
