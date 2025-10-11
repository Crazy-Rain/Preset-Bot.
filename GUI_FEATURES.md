# GUI Implementation - Visual Guide

## New Tabs Added to GUI

The GUI now includes two new tabs:

### 1. Lorebooks Tab

```
┌───────────────────────────────────────────────────────────────────────────┐
│                         Preset Discord Bot - GUI                           │
├──┬──────┬─────────┬────────┬──────────┬────────────┬──────────┬──────────┤
│  │Config│ Presets │ Manual │Characters│User Chars  │Lorebooks │ Console  │
├──┴──────┴─────────┴────────┴──────────┴────────────┴──────────┴──────────┤
│                                                                            │
│  ┌─────────────────────┬────────────────────────────────────────────┐    │
│  │ Lorebook Management │        Entry Management                     │    │
│  ├─────────────────────┴────────────────────────────────────────────┤    │
│  │                     │                                              │    │
│  │ New Lorebook:       │  Selected: fantasy_world                     │    │
│  │ [____________] [Create]                                            │    │
│  │                     │  ┌─────────────────────────────────────┐   │    │
│  │ ┌─────────────────┐ │  │ Add/Edit Entry                      │   │    │
│  │ │ ✓ fantasy_world │ │  │                                     │   │    │
│  │ │   (3 entries)   │ │  │ Content:                            │   │    │
│  │ │ ✗ sci_fi_univ.. │ │  │ ┌─────────────────────────────────┐ │   │    │
│  │ │                 │ │  │ │This is a high-fantasy medieval  │ │   │    │
│  │ │                 │ │  │ │world.                           │ │   │    │
│  │ │                 │ │  │ └─────────────────────────────────┘ │   │    │
│  │ │                 │ │  │                                     │   │    │
│  │ │                 │ │  │ Activation Type:                    │   │    │
│  │ │                 │ │  │  ◉ Constant (Always Active)        │   │    │
│  │ └─────────────────┘ │  │  ○ Normal (Keyword Triggered)      │   │    │
│  │                     │  │                                     │   │    │
│  │ [Activate]          │  │ Keywords:                           │   │    │
│  │ [Deactivate]        │  │ [dragon, dragons, wyrm___________] │   │    │
│  │ [Delete] [Refresh]  │  │ (comma-separated)                   │   │    │
│  │                     │  │                                     │   │    │
│  │                     │  │ [Add Entry] [Update] [Clear Form]  │   │    │
│  │                     │  └─────────────────────────────────────┘   │    │
│  │                     │                                              │    │
│  │                     │  ┌─────────────────────────────────────┐   │    │
│  │                     │  │ Entries in Selected Lorebook        │   │    │
│  │                     │  ├─────────────────────────────────────┤   │    │
│  │                     │  │ [C] This is a high-fantasy medie... │   │    │
│  │                     │  │ [N] Dragons are wise, ancient be... │   │    │
│  │                     │  │     [dragon, dragons]                │   │    │
│  │                     │  │ [N] Elves live in forest cities.    │   │    │
│  │                     │  │     [elf, elves]                     │   │    │
│  │                     │  │                                      │   │    │
│  │                     │  └─────────────────────────────────────┘   │    │
│  │                     │  [Edit Selected] [Delete] [Refresh]         │    │
│  └─────────────────────┴────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- **Left Panel**: List of all lorebooks with active/inactive indicators (✓/✗)
- **Right Panel**: Entry management for selected lorebook
- **Create**: Add new lorebooks
- **Activate/Deactivate**: Toggle lorebook active state
- **Delete**: Remove lorebooks
- **Entry Types**: 
  - [C] = Constant (always active)
  - [N] = Normal (keyword triggered)
- **Keywords**: Shown for normal entries, comma-separated

### 2. Console Tab

```
┌───────────────────────────────────────────────────────────────────────────┐
│                         Preset Discord Bot - GUI                           │
├──┬──────┬─────────┬────────┬──────────┬────────────┬──────────┬──────────┤
│  │Config│ Presets │ Manual │Characters│User Chars  │Lorebooks │ Console  │
├──┴──────┴─────────┴────────┴──────────┴────────────┴──────────┴──────────┤
│                                                                            │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ AI Request/Response Console                                        │  │
│  ├────────────────────────────────────────────────────────────────────┤  │
│  │                                                                     │  │
│  │ [2025-10-11 12:37:00] Console initialized. AI requests and        │  │
│  │                       responses will appear here.                  │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:37:05] Testing OpenAI connection...                │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:37:06] Sending test request to                     │  │
│  │                       https://api.openai.com/v1                    │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:37:08] Response received: Connection successful!   │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:38:00] Preparing to send manual message to         │  │
│  │                       channel 123456789 as assistant               │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:38:01] Message content: Hello, this is a test...   │  │
│  │                                                                     │  │
│  │ [2025-10-11 12:38:03] Message sent successfully to channel        │  │
│  │                       123456789 as Assistant                       │  │
│  │                                                                     │  │
│  │                                                                     │  │
│  │                                                                     │  │
│  │                                                                     │  │
│  │                                                                     │  │
│  │                                                                     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ☑ Auto-scroll   [Clear Console]   [Export Log]                          │
└───────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- **Timestamped Logs**: Each entry has a timestamp
- **Color Coding** (in actual GUI):
  - Blue: Headers
  - Green: Requests
  - Purple: Responses
  - Red: Errors
  - Gray: Info messages
  - Navy: Timestamps
- **Auto-scroll**: Checkbox to enable/disable auto-scrolling to latest entry
- **Clear Console**: Clear all log entries
- **Export Log**: Save console output to a text file

## How to Use

### Managing Lorebooks:

1. **Create a Lorebook**: Enter a name and click "Create"
2. **Select a Lorebook**: Click on a lorebook in the list
3. **Activate/Deactivate**: Select a lorebook and click the corresponding button
4. **Delete**: Select and click "Delete" (with confirmation)

### Managing Entries:

1. **Add Entry**:
   - Enter content in the text area
   - Select activation type (Constant or Normal)
   - If Normal, enter comma-separated keywords
   - Click "Add Entry"

2. **Edit Entry**:
   - Select an entry from the list
   - Click "Edit Selected"
   - Modify the content/type/keywords
   - Click "Update Entry"

3. **Delete Entry**:
   - Select an entry
   - Click "Delete Selected" (with confirmation)

### Using the Console:

- The console automatically logs all AI interactions
- Use Auto-scroll to keep the latest entries visible
- Export logs for debugging or record-keeping
- Clear when the console gets too long

## Entry Types Explained

### Constant Entries
- **Always Active**: Sent with every AI request when the lorebook is active
- **Use Case**: Core world information, character backgrounds, general rules
- **Example**: "This is a high-fantasy medieval world with magic."

### Normal (Keyword-Triggered) Entries
- **Conditionally Active**: Only sent when keywords match the user's message
- **Use Case**: Specific information about characters, locations, items
- **Example**: "Dragons are ancient, wise creatures." (keywords: dragon, dragons)

### Visual Indicators

- **✓** = Active lorebook (entries will be used)
- **✗** = Inactive lorebook (entries will be ignored)
- **[C]** = Constant entry (always included)
- **[N]** = Normal entry (keyword-triggered)
