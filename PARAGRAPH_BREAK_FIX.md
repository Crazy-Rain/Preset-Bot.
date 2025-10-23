# Fix for Bot Stopping on Paragraph Breaks

## Issue Description
Users reported that the bot stops processing when a message is sent with a paragraph break (pressing Enter twice to create a blank line between text).

Example problematic input:
```
!chat Character: First line

Second line after paragraph break
```

## Root Cause
The issue stems from Discord.py's command parser behavior when handling the `*, message: str` parameter (greedy string converter) with messages containing certain newline patterns. When the parser fails to correctly extract the message parameter, it raises a `MissingRequiredArgument` exception that wasn't being caught, causing the bot to stop processing commands.

## Solution Implemented

### 1. Added Command Error Handler (`bot.py`)
Added an `on_command_error` event handler that gracefully catches and handles various command parsing errors:

- **MissingRequiredArgument**: Provides helpful usage instructions when the message parameter is missing
- **BadArgument**: Handles invalid argument types
- **CommandNotFound**: Silently ignores (might be for another bot)
- **Other errors**: Logs to console without exposing internal errors to users

```python
@self.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'message':
            await ctx.send("Please provide a message after the command...")
    # ... other error handling
```

### 2. Added Message Validation (`bot.py`)
Added validation at the start of the `!chat` command to check for empty or whitespace-only messages:

```python
# Validate that message is not empty or only whitespace
if not message or not message.strip():
    await ctx.send("Please provide a message. Usage: `!chat [character]: your message here`")
    return
```

This prevents the bot from processing messages that contain only newlines or whitespace.

### 3. Comprehensive Testing
Created `test_paragraph_break_handling.py` with tests for:
- Command error handler registration
- MissingRequiredArgument error handling
- Paragraph breaks in message strings
- Various newline patterns (single, double, leading, trailing, etc.)
- Edge cases (empty strings, whitespace-only messages)

## Testing Results

All tests pass successfully:
- ✅ Existing message splitting tests (8/8)
- ✅ Existing bot tests (5/5)
- ✅ New paragraph break handling tests (4/4)

## Supported Newline Patterns

The fix properly handles all of the following message patterns:

| Pattern | Example | Valid? |
|---------|---------|--------|
| Single newline | `Line 1\nLine 2` | ✅ |
| Paragraph break | `Para 1\n\nPara 2` | ✅ |
| Triple newline | `Text\n\n\nMore` | ✅ |
| Leading newline | `\nText` | ✅ |
| Leading paragraph | `\n\nText` | ✅ |
| Trailing newline | `Text\n` | ✅ |
| Trailing paragraph | `Text\n\n` | ✅ |
| Mixed | `Start\n\nMid\nEnd` | ✅ |
| Only newlines | `\n\n` | ❌ (rejected) |
| Only whitespace | `   ` | ❌ (rejected) |
| Empty | `` | ❌ (rejected) |

## Benefits

1. **Robustness**: Bot no longer stops on command parsing errors
2. **User Experience**: Users receive helpful feedback instead of silence
3. **Debugging**: Command errors are logged for troubleshooting
4. **Maintainability**: Comprehensive tests prevent regressions

## Security

- No security vulnerabilities introduced
- CodeQL analysis: 0 alerts
- No sensitive data exposed in error messages
- Proper error handling prevents information leakage

## Backward Compatibility

- All existing tests pass
- No breaking changes to command syntax
- Existing functionality preserved
- Only adds error handling and validation
