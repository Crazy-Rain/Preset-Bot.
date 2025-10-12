# Quick Reference: Lorebook Visibility Improvements

## What Changed?

### Console Logging (Code-Side Visibility)
When the bot processes lorebooks, you'll now see clear console output:

```
[Lorebook] Processing 'fantasy_world' - ACTIVE
[Lorebook] Added 2 entries from 'fantasy_world'
[Lorebook] Skipping 'scifi_world' - INACTIVE
```

**What this tells you:**
- Which lorebooks are active vs inactive
- Which lorebooks contributed entries to the AI response
- How many entries each active lorebook added

### GUI Enhancements (Visual Visibility)

#### 1. Color-Coded Lorebook List
- **Active lorebooks**: Shown in **GREEN** text
- **Inactive lorebooks**: Shown in **GRAY** text
- **Text format**: `✓ ACTIVE | name (X entries)` or `✗ INACTIVE | name (X entries)`

#### 2. Status Indicator
When you select a lorebook, a colored status box appears:

- **Active**: Green background, "STATUS: ACTIVE ✓"
- **Inactive**: Red background, "STATUS: INACTIVE ✗"

## How to Use

### Checking Lorebook Status

**In GUI:**
1. Open the Lorebooks tab
2. Look at the list - green = active, gray = inactive
3. Click a lorebook to see its large status indicator

**In Console:**
- Start the bot normally
- Send a message in Discord
- Check the console for `[Lorebook]` messages
- You'll see which lorebooks were used

### Activating/Deactivating Lorebooks

**In GUI:**
1. Select a lorebook from the list
2. Click "Activate" or "Deactivate" button
3. **Immediately see the change:**
   - List item changes color (green ↔ gray)
   - Status indicator updates
4. No bot restart needed!

**Via Discord Commands:**
```
!lorebook activate lorebook_name
!lorebook deactivate lorebook_name
!lorebook list  (shows current status of all lorebooks)
```

### Verifying It Works

**Test Active Lorebook:**
1. Make sure lorebook is activated (green in GUI)
2. Send a test message in Discord
3. Check console: Should see `[Lorebook] Processing 'name' - ACTIVE`
4. AI response should include lorebook content

**Test Inactive Lorebook:**
1. Deactivate the lorebook (turns gray in GUI)
2. Send the same test message
3. Check console: Should see `[Lorebook] Skipping 'name' - INACTIVE`
4. AI response should NOT include lorebook content

## Common Scenarios

### "Is my lorebook being used?"
✅ **Check console output** - Look for `[Lorebook] Processing 'name' - ACTIVE`
✅ **Check GUI** - Lorebook should be green with "STATUS: ACTIVE ✓"

### "I deactivated a lorebook but it's still being used"
1. Check GUI - Is it actually gray/inactive?
2. Check console - Should show `[Lorebook] Skipping 'name' - INACTIVE`
3. If not, the lorebook might be re-activated - check the status

### "I want to temporarily disable all lorebooks"
1. Go to GUI → Lorebooks tab
2. Select each green (active) lorebook
3. Click "Deactivate" for each one
4. All should turn gray
5. Next AI response won't use any lorebook entries

### "I want to see which lorebooks contribute most"
1. Send a test message
2. Check console output
3. Look at the "Added X entries" counts
4. Higher numbers = more content from that lorebook

## Benefits

| Feature | Before | After |
|---------|--------|-------|
| **Visual Status** | Small ✓/✗ symbol | Color coded + explicit labels |
| **Selected Status** | No indicator | Large colored status box |
| **Code Visibility** | Silent processing | Console logs show everything |
| **Debugging** | Hard to tell what's happening | Clear logs show active/inactive |
| **Verification** | Need to test responses | Can see status immediately |

## Example Output

### Console Example
```
[Lorebook] Processing 'world_lore' - ACTIVE
[Lorebook] Added 3 entries from 'world_lore'
[Lorebook] Skipping 'old_campaign' - INACTIVE
[Lorebook] Processing 'character_info' - ACTIVE
[Lorebook] Added 1 entries from 'character_info'
```

**Interpretation:** 
- 'world_lore' is active, added 3 entries
- 'old_campaign' is inactive, was skipped
- 'character_info' is active, added 1 entry
- Total: 4 lorebook entries sent to AI

### GUI Example

**Lorebook List:**
```
✓ ACTIVE | world_lore (12 entries)         [shown in green]
✓ ACTIVE | character_info (5 entries)      [shown in green]
✗ INACTIVE | old_campaign (8 entries)      [shown in gray]
✗ INACTIVE | test_stuff (2 entries)        [shown in gray]
```

**Status Indicator (when 'world_lore' selected):**
```
┌───────────────────────┐
│  STATUS: ACTIVE ✓     │  [light green background]
└───────────────────────┘  [dark green text]
```

## Troubleshooting

**Q: I don't see console logs**
- Make sure you're running the bot from a terminal/console
- Logs appear when processing AI responses
- Send a message in Discord to trigger logging

**Q: GUI doesn't show colors**
- This is a visual enhancement - basic functionality still works
- Check if your terminal/system supports colors
- The text labels (ACTIVE/INACTIVE) are still there

**Q: Colors are wrong**
- Make sure you're using the latest version
- Try restarting the GUI
- Check if lorebook is actually active/inactive in config.json

## Testing

Run the demonstration script to see everything in action:

```bash
python demo_visibility_improvements.py
```

This shows:
1. Console logging examples
2. GUI enhancement descriptions
3. Complete workflow demonstration

## Files Changed

- `bot.py` - Added console logging
- `gui.py` - Added color coding and status indicator
- `LOREBOOK_VISIBILITY_IMPROVEMENTS.md` - Full documentation
- `demo_visibility_improvements.py` - Demonstration script
- `test_gui_visibility.py` - Test script

## Summary

**The Problem:** Hard to tell if activate/deactivate was working
**The Solution:** Clear visual and console indicators
**The Result:** Immediately obvious which lorebooks are active/inactive

No more guessing - you can now **see exactly** what the bot is doing with your lorebooks!
