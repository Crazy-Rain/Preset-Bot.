# GUI Error Handling and Console Logging Improvements

## Summary of Changes

This update addresses three critical issues reported in the problem statement:

1. **X11 Fatal IO Error**: GUI closing unexpectedly with connection reset errors
2. **Console not showing errors/responses**: No visibility into bot operations
3. **!chat command silent failures**: Commands failing without user feedback

## Changes Made

### 1. GUI Exception Handling (`gui.py`)

#### Window Close Handler
- Added `WM_DELETE_WINDOW` protocol handler to gracefully close the GUI
- Prevents X11 fatal IO errors by properly cleaning up resources
- Safely stops Discord client before destroying the window

```python
def on_closing(self):
    """Handle window close event gracefully"""
    try:
        # Stop any running Discord client
        if self.discord_client and not self.discord_client.is_closed():
            self.discord_client.close()
    except Exception as e:
        print(f"Error closing Discord client: {str(e)}")
    finally:
        self.root.destroy()
```

#### Main Loop Exception Handling
- Wrapped main GUI initialization in try-except block
- Catches and logs fatal errors instead of crashing silently
- Shows error dialog to user with details

```python
def main():
    """Main entry point for GUI"""
    try:
        root = tk.Tk()
        app = PresetBotGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Fatal error in GUI: {str(e)}")
        print(traceback.format_exc())
        try:
            messagebox.showerror("Fatal Error", 
                f"The application encountered a fatal error:\n{str(e)}")
        except:
            pass
```

### 2. Console Logging Integration (`bot.py`)

#### AIResponseHandler Logging Callback
- Added `set_log_callback()` method to route logs to GUI console
- Added internal `_log()` method that uses callback when available
- Falls back to `print()` when no callback is set (bot-only mode)
- Exception handling prevents callback errors from crashing the bot

```python
def set_log_callback(self, callback):
    """Set a callback function for logging (e.g., to GUI console)"""
    self.log_callback = callback

def _log(self, message, tag='info'):
    """Internal logging method that uses callback if available"""
    if self.log_callback:
        try:
            self.log_callback(message, tag)
        except Exception as e:
            print(f"Error in log callback: {str(e)}")
    else:
        print(message)
```

#### AI Request/Response Logging
- Logs AI requests before sending to OpenAI
- Logs successful responses when received
- Logs errors when API calls fail

```python
# In get_ai_response():
self._log(f"Sending AI request to model '{model}' with message: {message[:100]}...", 'request')

# After receiving response:
self._log(f"Received AI response: {response_text[:200]}...", 'response')

# On error:
self._log(error_msg, 'error')
```

### 3. Chat Command Error Handling (`bot.py`)

#### Comprehensive Try-Except Block
- Wrapped entire `!chat` command in try-except
- Catches all exceptions and reports them to user
- Logs full stack trace to console for debugging

```python
@self.command(name='chat')
async def chat(ctx, user_character: Optional[str] = None, *, message: str):
    try:
        # ... existing chat logic ...
    except Exception as e:
        error_msg = f"Error in chat command: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        await ctx.send(f"An error occurred while processing your chat message: {str(e)}")
```

## Benefits

### For Users
- **No more silent crashes**: GUI shows error messages instead of dying
- **Visibility into bot operations**: Console tab shows all AI requests/responses
- **Better error messages**: Chat command failures are reported with details

### For Debugging
- **Full logging**: Every AI interaction is logged with timestamps
- **Stack traces**: Errors include full context for troubleshooting
- **Console export**: All logs can be exported to file for analysis

## How to Use

### Running the GUI
```bash
python gui.py
```

The GUI will now:
1. Handle X11 errors gracefully without crashing
2. Show all AI requests/responses in the Console tab
3. Display error messages when things go wrong

### Viewing Console Logs
1. Open the GUI
2. Navigate to the "Console" tab
3. Watch for real-time logs as you:
   - Test OpenAI connection
   - Send manual messages
   - Use bot commands

### Log Types in Console
- **Blue timestamps**: When each event occurred
- **Green (request)**: AI requests being sent
- **Purple (response)**: AI responses received
- **Red (error)**: Errors and failures
- **Gray (info)**: General information

### Exporting Logs
1. Click "Export Log" button in Console tab
2. Choose file location
3. Save complete console history for debugging

## Testing

Run the test suite to verify all improvements:
```bash
python /tmp/test_logging_improvements.py
```

This verifies:
- ✓ Logging callback mechanism works
- ✓ Fallback to print() when GUI not available
- ✓ Exception handling in callbacks
- ✓ All log types (info, request, response, error)

## Compatibility

- **Bot-only mode**: Works without GUI (falls back to print)
- **GUI mode**: Full console logging with visual interface
- **No breaking changes**: Existing functionality preserved
