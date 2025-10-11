# Quick Start Guide: New GUI Features

## Two New Tabs Added! 🎉

The Preset Bot GUI now includes:
1. **Lorebooks Tab** - Manage lorebooks and entries
2. **Console Tab** - View AI request/response logs

## Starting the GUI

```bash
python3 start.py
# Choose option 1: Run Configuration GUI
```

## Using the Lorebooks Tab

### Create a Lorebook
1. Click the **Lorebooks** tab
2. Enter a name in "New Lorebook" field
3. Click **Create**
4. Your lorebook appears with ✓ (active)

### Add a Constant Entry (Always Active)
1. Select your lorebook from the list
2. Enter content in the text area
3. Select **⦿ Constant (Always Active)**
4. Click **Add Entry**

### Add a Keyword-Triggered Entry
1. Select your lorebook from the list
2. Enter content in the text area
3. Select **⦿ Normal (Keyword Triggered)**
4. Enter keywords separated by commas: `dragon, dragons, wyrm`
5. Click **Add Entry**

### Edit an Entry
1. Select an entry from the list
2. Click **Edit Selected**
3. Modify the content/type/keywords
4. Click **Update Entry**

### Activate/Deactivate a Lorebook
1. Select a lorebook from the list
2. Click **Activate** or **Deactivate**
3. Status updates: ✓ = active, ✗ = inactive

## Using the Console Tab

### View Logs
1. Click the **Console** tab
2. All AI operations appear automatically

### Auto-scroll
- Check **☑ Auto-scroll** to follow the latest entries

### Clear Logs
- Click **Clear Console** to remove all entries

### Export Logs
- Click **Export Log** to save to a text file

## Visual Indicators

### In Lorebook List:
- **✓** = Active lorebook (entries will be used)
- **✗** = Inactive lorebook (entries will be ignored)
- **(3 entries)** = Number of entries in lorebook

### In Entry List:
- **[C]** = Constant entry (always included)
- **[N]** = Normal entry (keyword-triggered)
- **[dragon, wyrm]** = Keywords for normal entries

## Example: Creating a Fantasy World

```
1. Create lorebook: "fantasy_world"

2. Add constant entry:
   Content: "This is a high-fantasy medieval world with magic."
   Type: Constant
   
3. Add keyword entries:
   Content: "Dragons are rare, powerful creatures."
   Type: Normal
   Keywords: dragon, dragons, wyrm
   
   Content: "Elves live in harmony with nature."
   Type: Normal
   Keywords: elf, elves, elven
```

**Result:**
- Message: "Hello" → 1 entry sent (constant only)
- Message: "Tell me about dragons" → 2 entries sent (constant + dragon)
- Message: "Dragons and elves?" → 3 entries sent (all)

## Console Log Examples

```
[2025-10-11 12:37:00] Console initialized. AI requests and responses will appear here.
[2025-10-11 12:37:05] Testing OpenAI connection...
[2025-10-11 12:37:06] Sending test request to https://api.openai.com/v1
[2025-10-11 12:37:08] Response received: Connection successful!
[2025-10-11 12:38:00] Preparing to send manual message to channel 123456789
[2025-10-11 12:38:03] Message sent successfully to channel 123456789
```

## Tips

- **Multiple Lorebooks**: You can have multiple lorebooks active at the same time
- **Keywords**: Use lowercase for keywords (matching is case-insensitive)
- **Console**: Export logs before clearing if you need to save them
- **Testing**: Use the "Test OpenAI Connection" button to see console logging in action

## Need Help?

See detailed documentation:
- **LOREBOOK_GUI_README.md** - Complete usage guide
- **GUI_FEATURES.md** - Visual layouts
- **demo_integration.py** - Code examples

Run demos:
```bash
python3 demo_integration.py  # Full workflow demo
python3 test_gui_lorebooks.py  # Test operations
```

## That's It! 🎉

You now have powerful lorebook management and AI logging right in the GUI!
