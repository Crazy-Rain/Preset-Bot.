# Lorebook and Console GUI Features - Implementation Complete

## Overview

This PR adds two major features to the Preset Bot GUI as requested:

1. **Lorebook Management Tab** - Complete CRUD interface for lorebooks and entries
2. **Console Tab** - Real-time logging of AI requests and responses

## What's New

### 1. Lorebooks Tab

A comprehensive interface for managing lorebooks and their entries, similar to SillyTavern's implementation.

#### Features:
- **Create/Delete Lorebooks** - Add new lorebooks or remove existing ones
- **Activate/Deactivate** - Toggle which lorebooks are active for AI responses
- **Entry Management** - Add, edit, and delete entries within lorebooks
- **Activation Types**:
  - **Constant**: Always included when lorebook is active
  - **Normal**: Only included when keywords match the user's message
- **Keywords**: Comma-separated keyword input for normal entries
- **Visual Indicators**: See at a glance which lorebooks and entries are active

#### UI Layout:
```
┌─────────────────────────────────────────────────────────┐
│ Left Panel          │  Right Panel                      │
├─────────────────────┼───────────────────────────────────┤
│ Lorebook List       │  Selected Lorebook: fantasy_world │
│ ✓ fantasy_world (3) │                                   │
│ ✗ sci_fi (2)        │  Entry Editor:                    │
│                     │  - Content (text area)            │
│ [Create]            │  - Type: ⦿ Constant ○ Normal     │
│ [Activate]          │  - Keywords: dragon, wyrm         │
│ [Deactivate]        │  [Add Entry] [Update] [Clear]     │
│ [Delete]            │                                   │
│                     │  Entry List:                      │
│                     │  [C] High-fantasy world...        │
│                     │  [N] Dragons are rare... [dragon] │
│                     │  [Edit] [Delete] [Refresh]        │
└─────────────────────┴───────────────────────────────────┘
```

### 2. Console Tab

Real-time logging of all AI interactions and operations.

#### Features:
- **Timestamped Logs** - Every entry includes date/time
- **Color Coding**:
  - 🔵 Blue: Headers
  - 🟢 Green: Requests
  - 🟣 Purple: Responses
  - 🔴 Red: Errors
  - ⚪ Gray: Info
  - 🔷 Navy: Timestamps
- **Auto-scroll** - Optionally scroll to latest entries
- **Export Logs** - Save console to text file
- **Clear Console** - Clear all entries

#### What Gets Logged:
- OpenAI connection tests
- Manual message sends
- AI requests and responses
- Lorebook operations
- Errors and warnings

## How to Use

### Managing Lorebooks

1. **Create a Lorebook**:
   - Switch to "Lorebooks" tab
   - Enter a name in "New Lorebook" field
   - Click "Create"
   - Lorebook appears in list with ✓ (active)

2. **Add Constant Entry** (always active):
   - Select a lorebook from the list
   - Enter content in the text area
   - Select "Constant (Always Active)"
   - Click "Add Entry"

3. **Add Normal Entry** (keyword-triggered):
   - Select a lorebook from the list
   - Enter content in the text area
   - Select "Normal (Keyword Triggered)"
   - Enter comma-separated keywords
   - Click "Add Entry"

4. **Edit Entry**:
   - Select an entry from the list
   - Click "Edit Selected"
   - Modify content/type/keywords
   - Click "Update Entry"

5. **Delete Entry**:
   - Select an entry
   - Click "Delete Selected"
   - Confirm deletion

6. **Activate/Deactivate Lorebook**:
   - Select a lorebook
   - Click "Activate" or "Deactivate"
   - Status updates (✓ = active, ✗ = inactive)

### Using the Console

The console automatically logs all operations. No setup required!

- **View Logs**: Switch to "Console" tab
- **Auto-scroll**: Check "Auto-scroll" to follow latest entries
- **Clear**: Click "Clear Console" to remove all entries
- **Export**: Click "Export Log" to save to file

## Technical Details

### Files Modified:
- `gui.py` - Added lorebooks and console tabs (+481 lines)

### Files Created:
- `test_gui_lorebooks.py` - Test suite for GUI operations
- `demo_gui.py` - Standalone GUI demo
- `demo_integration.py` - Integration workflow demo
- `GUI_FEATURES.md` - Visual documentation

### Backend Integration:

The GUI uses existing `ConfigManager` methods from `bot.py`:

**Lorebook Management:**
- `get_lorebooks()` - Retrieve all lorebooks
- `add_lorebook(name, active)` - Create new lorebook
- `update_lorebook(index, name, active)` - Update lorebook
- `delete_lorebook(index)` - Remove lorebook
- `toggle_lorebook_active(name, active)` - Toggle active state

**Entry Management:**
- `add_lorebook_entry(lorebook_name, content, insertion_type, keywords)` - Add entry
- `update_lorebook_entry(lorebook_name, entry_index, content, insertion_type, keywords)` - Update entry
- `delete_lorebook_entry(lorebook_name, entry_index)` - Remove entry
- `get_active_lorebook_entries(message)` - Get entries for AI context

All backend functionality was already implemented - this PR only adds the GUI!

## Testing

All tests pass:
```bash
$ python3 -m pytest test_lorebook.py test_lorebook_integration.py test_gui_lorebooks.py -v

test_lorebook.py::test_lorebook_management PASSED              [ 16%]
test_lorebook.py::test_lorebook_entries PASSED                 [ 33%]
test_lorebook.py::test_active_lorebook_entries PASSED          [ 50%]
test_lorebook.py::test_config_persistence PASSED               [ 66%]
test_lorebook_integration.py::test_lorebook_ai_integration PASSED [ 83%]
test_gui_lorebooks.py::test_lorebook_gui_operations PASSED     [100%]

6 passed, 6 warnings in 0.68s
```

### Demo Scripts:

Run these to see the features in action:

```bash
# Test backend operations
python3 test_gui_lorebooks.py

# See integration workflow
python3 demo_integration.py

# View GUI layout (requires tkinter)
python3 demo_gui.py
```

## Examples

### Example 1: Fantasy World Setup

```python
# Create lorebook
lorebook = "fantasy_world"

# Add constant entry (always included)
add_lorebook_entry(lorebook, 
    "This is a high-fantasy medieval world.", 
    "constant")

# Add keyword entries
add_lorebook_entry(lorebook,
    "Dragons are rare, powerful creatures.",
    "normal", 
    ["dragon", "dragons", "wyrm"])

add_lorebook_entry(lorebook,
    "Elves live in forest cities.",
    "normal",
    ["elf", "elves", "elven"])
```

**Result:**
- Message: "Hello" → 1 entry (constant)
- Message: "Tell me about dragons" → 2 entries (constant + dragon)
- Message: "Are there elves and dragons?" → 3 entries (all)

### Example 2: Multiple Lorebooks

```python
# Create multiple lorebooks
add_lorebook("fantasy_world", active=True)
add_lorebook("sci_fi_universe", active=False)

# Add entries to each...

# Only fantasy_world entries are used (active)
# sci_fi_universe entries are ignored (inactive)

# Toggle anytime:
toggle_lorebook_active("fantasy_world", False)
toggle_lorebook_active("sci_fi_universe", True)
```

## Benefits

### For Users:
- ✅ Easy visual management of lorebooks
- ✅ See exactly what's being sent to the AI
- ✅ Debug issues with console logs
- ✅ No command-line needed for lorebook management

### For Developers:
- ✅ All operations logged for debugging
- ✅ Export logs for issue reports
- ✅ Reuses existing backend (no duplication)
- ✅ Comprehensive test coverage

## Backward Compatibility

✅ **100% backward compatible**
- Existing config files work unchanged
- All existing commands still work
- No breaking changes
- All tests pass

## Documentation

- **GUI_FEATURES.md** - Visual guide with ASCII mockups
- **Demo scripts** - Working examples
- **Inline comments** - Code documentation
- **This README** - Complete usage guide

## Screenshots

See `GUI_FEATURES.md` for detailed ASCII mockups of both tabs.

## Known Limitations

- GUI requires `python3-tk` to be installed
- Console logs are not persisted (export to save)
- No search/filter in console (planned for future)

## Future Enhancements

Potential improvements:
- Search/filter console logs
- Import/export lorebooks
- Bulk edit entries
- Entry templates
- Lorebook presets

## Questions?

See the documentation files:
- `GUI_FEATURES.md` - Visual guide
- `LOREBOOK_IMPLEMENTATION.md` - Backend details
- `demo_integration.py` - Usage examples

Or run the demos:
```bash
python3 demo_gui.py          # GUI layout demo
python3 demo_integration.py  # Workflow demo
python3 test_gui_lorebooks.py # Test all operations
```
