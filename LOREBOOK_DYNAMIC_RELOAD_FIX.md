# Lorebook Dynamic Reload Fix

## Problem

When lorebooks were deactivated via the GUI, the Discord bot continued to use them in AI responses. This was confusing because users would:
1. Deactivate lorebooks in the GUI
2. Save the changes
3. Send messages in Discord
4. Still see lorebook entries being used in responses
5. The `!lorebook list` command would also show stale data

## Root Cause

The issue was caused by configuration caching:

1. **Config Caching**: When the bot starts, it loads `config.json` into memory
2. **GUI Changes**: The GUI modifies lorebooks and saves to `config.json` 
3. **Stale Data**: The bot's in-memory config becomes stale
4. **Incomplete Reload**: While commands (`!chat`, `!ask`, `!manualsend`) called `reload_config()`, the actual AI response generation happened in `get_ai_response()` which didn't reload
5. **Stale Command Data**: The `!lorebook` command also read from cached config

### Code Flow (Before Fix)

```
User runs !chat command
  ├─> Command handler calls reload_config() ✓
  ├─> Command handler calls get_ai_response()
  │     ├─> get_ai_response() reads lorebooks from cached config ✗
  │     └─> Uses stale lorebook states
  └─> Response includes deactivated lorebook entries

User runs !lorebook list
  ├─> Command reads from cached config ✗
  └─> Shows stale lorebook states
```

## Solution

Added `reload_config()` calls to ensure methods always use the latest configuration:

1. At the start of `get_ai_response()` method (for AI responses)
2. At the start of `!lorebook` command handler (for lorebook management)

### Code Changes

**File: `bot.py` - Fix 1: AI Response Generation**
```python
async def get_ai_response(self, message: str, ...):
    """Get AI response for a message"""
    if not self.client:
        return "Error: OpenAI API not configured..."
    
    # Reload config to get latest lorebook/character updates from GUI or other sources
    self.config_manager.reload_config()  # ← NEW LINE
    
    # ... rest of the method
```

**File: `bot.py` - Fix 2: Lorebook Command**
```python
@self.command(name='lorebook')
async def lorebook(ctx, action: str, *args):
    """Manage lorebooks"""
    # Reload config to get latest lorebook updates from GUI
    self.config_manager.reload_config()  # ← NEW LINE
    
    action = action.lower()
    # ... rest of the command
```

### Code Flow (After Fix)

```
User runs !chat command
  ├─> Command handler calls reload_config() ✓
  ├─> Command handler calls get_ai_response()
  │     ├─> get_ai_response() calls reload_config() ✓
  │     ├─> Reads fresh lorebook states from config file
  │     └─> Uses current lorebook states
  └─> Response correctly excludes deactivated lorebook entries

User runs !lorebook list
  ├─> Command calls reload_config() ✓
  ├─> Reads fresh lorebook states from config file
  └─> Shows current lorebook states
```

## Testing

### New Test: `test_lorebook_dynamic_reload.py`

Created comprehensive tests to verify:

1. **Dynamic Reload**: Lorebook changes made externally (by GUI) are picked up
2. **Active/Inactive Filtering**: Deactivated lorebooks don't contribute entries
3. **Multiple Lorebooks**: Different states are handled correctly
4. **Cache Behavior**: Without reload, cached data is used; with reload, fresh data is used

### Test Results

```
✅ All existing tests pass (4/4 lorebook tests)
✅ New dynamic reload tests pass (2/2 tests)
✅ Integration tests pass (1/1 tests)
```

## User Impact

### Before Fix
- Deactivating lorebooks in GUI had no effect
- Users had to restart the bot for changes to take effect
- Confusing and frustrating user experience

### After Fix
- Lorebook changes in GUI take effect immediately
- No bot restart required
- Deactivated lorebooks are correctly excluded from responses
- Dynamic, real-time configuration

## Performance Impact

Minimal - `reload_config()` just reads a JSON file from disk, which is very fast. This happens once per AI request, which is already a relatively slow operation (API call).

## Related Files

- `bot.py`: Main fix location
- `test_lorebook_dynamic_reload.py`: Test coverage for the fix
- `test_lorebook.py`: Existing tests (still pass)
- `test_lorebook_integration.py`: Integration tests (still pass)

## Verification

To verify the fix works:

1. Start the bot
2. Open the GUI and create a lorebook with constant entries
3. Activate the lorebook
4. Send a message in Discord - lorebook entries should appear in response
5. Deactivate the lorebook in GUI (don't restart bot)
6. Send another message - lorebook entries should NOT appear
7. No bot restart needed!

## Additional Benefits

This fix also ensures that other configuration changes (like character updates, preset changes, etc.) are picked up dynamically when generating AI responses, improving the overall responsiveness of the system.
