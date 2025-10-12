# Embed Description Splitting - Quick Reference

## What Was Fixed

Discord API error when viewing characters with long descriptions:
```
discord.errors.HTTPException: 400 Bad Request (error code: 50035)
Invalid Form Body: Must be 4096 or fewer in length
```

## The Solution

Character descriptions and scenarios exceeding 4096 characters are now automatically split into multiple embeds.

## How It Works

### Short Descriptions (≤ 4096 characters)
```
User clicks "Show Description"
         ↓
Single embed sent with complete description
```

### Long Descriptions (> 4096 characters)
```
User clicks "Show Description"
         ↓
Description split into chunks at sentence boundaries
         ↓
Multiple embeds sent in sequence:
  - "Description (Part 1/N)"
  - "Description (Part 2/N)"
  - etc.
```

## Commands Fixed

- **!viewc** - View AI Character
  - ✓ Show Description button
  - ✓ Show Scenario button

- **!viewu** - View User Character
  - ✓ Show Description button

## Technical Details

- **Limit**: 4096 characters (Discord embed description limit)
- **Chunk Size**: 4000 characters (96-char safety margin)
- **Splitting**: Intelligent sentence boundary detection
- **UX**: All parts appear instantly when button is clicked

## Files Modified

- `bot.py` - 3 button callbacks updated with splitting logic

## Files Added

- `test_embed_description_splitting.py` - Unit tests
- `test_embed_integration.py` - Integration tests
- `EMBED_DESCRIPTION_FIX.md` - Full technical documentation
- `VISUAL_EMBED_FIX.md` - Visual guide with diagrams
- `CHANGES_SUMMARY_EMBED_FIX.md` - Complete change summary

## Testing

All tests pass:
```
✅ test_embed_description_splitting.py - 5/5 tests passed
✅ test_embed_integration.py - 3/3 tests passed
✅ test_message_splitting.py - 8/8 tests passed (existing)
✅ bot.py - Valid Python syntax
```

## Benefits

✅ No more API errors for long descriptions
✅ Users can view complete character information
✅ Intelligent splitting preserves readability
✅ Backward compatible - short descriptions unchanged
✅ No changes needed to existing character data

## Example

**Before:**
- Character with 6000-char description → ❌ Error

**After:**
- Character with 6000-char description → ✅ 2 embeds sent
  - Part 1: ~4000 characters
  - Part 2: ~2000 characters

## See Also

- `MESSAGE_SPLITTING.md` - Original message splitting feature
- `IMPLEMENTATION_MESSAGE_SPLITTING_FIX.md` - Related implementation
