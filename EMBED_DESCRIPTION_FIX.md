# Embed Description Splitting Fix

## Problem

Users were encountering a Discord API error when clicking the "Show Description" button for AI Characters with very long descriptions:

```
discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In data.embeds.0.description: Must be 4096 or fewer in length.
```

This occurred because Discord has a hard limit of **4096 characters** for embed descriptions, and some character descriptions exceeded this limit.

## Solution

Implemented automatic splitting of long descriptions and scenarios using the existing `split_text_intelligently()` function. When a description or scenario exceeds 4096 characters, it is now split into multiple embeds that are sent sequentially.

### Changes Made

#### 1. **`viewc` Command - CharacterView**
   - **Show Description Button**: Now splits descriptions longer than 4096 characters
   - **Show Scenario Button**: Now splits scenarios longer than 4096 characters

#### 2. **`viewu` Command - DescriptionView**
   - **Show Description Button**: Now splits descriptions longer than 4096 characters

### Technical Details

- **Split Threshold**: 4096 characters (Discord's embed description limit)
- **Chunk Size**: 4000 characters (leaves 96-character safety margin)
- **Splitting Strategy**: Uses intelligent sentence boundary detection via `split_text_intelligently()`
- **User Experience**: 
  - Short descriptions (≤4096 chars): Single embed with title "Description"
  - Long descriptions (>4096 chars): Multiple embeds with titles "Description (Part 1/N)", "Description (Part 2/N)", etc.

### How It Works

1. **Check length**: If description ≤ 4096 characters, send as single embed
2. **Split if needed**: If description > 4096 characters, use `split_text_intelligently()` with max_chunk_size=4000
3. **Send first chunk**: Use `interaction.response.send_message()` for the first embed
4. **Send remaining chunks**: Use `interaction.followup.send()` for subsequent embeds

All embeds are sent as `ephemeral=True` (only visible to the user who clicked the button).

### Benefits

✅ **No more API errors** - All descriptions work regardless of length  
✅ **Intelligent splitting** - Breaks at sentence boundaries for readability  
✅ **Seamless UX** - Multiple embeds appear instantly in sequence  
✅ **Consistent behavior** - Same splitting logic used for AI responses  
✅ **Safety margin** - 4000 char chunks leave buffer below 4096 limit  

### Testing

Created comprehensive tests to validate the fix:

1. **test_embed_description_splitting.py** - Unit tests for splitting logic
   - Short descriptions (< 4096 chars)
   - Long descriptions (> 4096 chars)
   - Very long descriptions (> 8000 chars)
   - Edge cases (exactly 4096, 4097 chars)

2. **test_embed_integration.py** - Integration tests simulating button clicks
   - Normal length descriptions
   - Problem scenario (12,000+ character description)
   - Edge cases

All tests pass successfully.

### Code Changes

**File**: `bot.py`

**Lines Modified**:
- Lines 1262-1293: `viewu` command - DescriptionView.show_description()
- Lines 1390-1421: `viewc` command - CharacterView.show_description()
- Lines 1424-1454: `viewc` command - CharacterView.show_scenario()

**Files Added**:
- `test_embed_description_splitting.py` - Unit tests
- `test_embed_integration.py` - Integration tests

### Example

**Before** (Description > 4096 chars):
```
❌ Error: 400 Bad Request - Must be 4096 or fewer in length
```

**After** (Description > 4096 chars):
```
✅ Description (Part 1/3) - 3994 characters
✅ Description (Part 2/3) - 3999 characters  
✅ Description (Part 3/3) - 1050 characters
```

## Related

This fix uses the same intelligent splitting function (`split_text_intelligently()`) that was previously implemented for handling long AI response messages. The function ensures text is split at natural boundaries (sentences, paragraphs, or words) rather than mid-sentence.

See also:
- `MESSAGE_SPLITTING.md` - Documentation for the splitting algorithm
- `IMPLEMENTATION_MESSAGE_SPLITTING_FIX.md` - Original implementation details
