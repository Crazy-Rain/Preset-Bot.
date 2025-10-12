# Lorebook Importer - Quick Reference

## Quick Start

1. **Open Lorebooks Tab** in the GUI
2. Click **Import...** button
3. Select a JSON file containing lorebook data
4. Preview and select entries to import
5. Choose destination (existing or new lorebook)
6. Click **Import**

## Supported File Formats

### Single Lorebook
```json
{
  "name": "lorebook_name",
  "entries": [...]
}
```

### Config Format
```json
{
  "lorebooks": [
    {"name": "lb1", "entries": [...]},
    {"name": "lb2", "entries": [...]}
  ]
}
```

### Array Format
```json
[
  {"name": "lb1", "entries": [...]},
  {"name": "lb2", "entries": [...]}
]
```

## Entry Format

```json
{
  "content": "Entry text",
  "insertion_type": "constant",  // or "normal"
  "keywords": []  // for normal entries: ["keyword1", "keyword2"]
}
```

## Import Options

### Filter Entries
- **All Entries**: Show everything
- **Constant Only**: Show only always-active entries
- **Normal Only**: Show only keyword-triggered entries

### Select Entries
- Click entry to toggle checkbox (☑/☐)
- **Select All**: Check all visible entries
- **Deselect All**: Uncheck all entries

### Destination
- **Selected Lorebook**: Add to currently selected lorebook
- **New Lorebook**: Create new lorebook with specified name

## Common Use Cases

### Import from SillyTavern
1. Export lorebook from SillyTavern as JSON
2. Click Import in GUI
3. Select the exported file
4. Choose "New Lorebook" 
5. Import

### Merge Multiple Lorebooks
1. Select target lorebook in main GUI
2. Click Import
3. Load first source file
4. Select entries to import
5. Choose "Selected Lorebook"
6. Repeat for additional files

### Import Only Specific Entry Types
1. Click Import
2. Select file
3. Use filter: "Constant Only" or "Normal Only"
4. Click "Select All"
5. Import filtered entries

### Create Backup
To export: Save `config.json` (contains all lorebooks)
To restore: Use Import feature to load from backup

## Keyboard Shortcuts

None currently - use mouse clicks for all interactions.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Invalid JSON file" | Check JSON syntax with validator |
| "Invalid lorebook format" | Ensure file has "entries" or "lorebooks" field |
| "No entries selected" | Check at least one entry checkbox |
| "Select a lorebook first" | Click a lorebook in main window or use "New Lorebook" |
| No lorebooks shown | File may be empty or invalid format |

## Tips

✅ **Preview before importing** - Always review entries first
✅ **Use filters** - Filter by type to import only what you need  
✅ **Test with small files** - Start with small lorebooks to test  
✅ **Backup first** - Save config.json before major imports  
✅ **Check duplicates** - Importer doesn't check for duplicate entries

## Feature Highlights

- ✨ Import from multiple file formats
- ✨ Preview all entries before importing
- ✨ Filter by entry type (constant/normal)
- ✨ Selective import with checkboxes
- ✨ Import to existing or new lorebook
- ✨ Bulk import multiple entries at once
- ✨ Clear error messages for invalid files
