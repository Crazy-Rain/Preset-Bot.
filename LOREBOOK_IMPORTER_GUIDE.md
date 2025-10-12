# Lorebook Importer Feature

## Overview

The Lorebook Importer allows you to bulk-import lorebook entries from external JSON files into your existing lorebooks or create new ones. This feature is useful for:

- Importing lorebooks from other applications (like SillyTavern)
- Backing up and restoring lorebooks
- Sharing lorebooks between different instances
- Bulk-adding entries without manual input

## How to Use

### 1. Access the Importer

1. Open the GUI application
2. Navigate to the **Lorebooks** tab
3. Click the **Import...** button in the Lorebook Management section

### 2. Select a Lorebook File

The importer supports multiple JSON formats:

**Single Lorebook Format:**
```json
{
  "name": "fantasy_world",
  "active": true,
  "entries": [
    {
      "content": "Entry text here",
      "insertion_type": "constant",
      "keywords": []
    },
    {
      "content": "Another entry",
      "insertion_type": "normal",
      "keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

**Config File Format (Multiple Lorebooks):**
```json
{
  "lorebooks": [
    {
      "name": "lorebook1",
      "active": true,
      "entries": [...]
    },
    {
      "name": "lorebook2",
      "active": false,
      "entries": [...]
    }
  ]
}
```

**Array Format:**
```json
[
  {
    "name": "lorebook1",
    "entries": [...]
  },
  {
    "name": "lorebook2",
    "entries": [...]
  }
]
```

### 3. Preview and Filter Entries

The import preview dialog provides:

**Left Panel - Lorebook Selection:**
- Lists all lorebooks found in the file
- Shows entry count for each lorebook
- Click to preview entries

**Right Panel - Entry Preview:**
- Shows all entries from the selected lorebook
- Filter options:
  - **All Entries**: Show both constant and normal entries
  - **Constant Only**: Show only constant (always-active) entries
  - **Normal Only**: Show only keyword-triggered entries

**Entry Information:**
- **Type**: CONSTANT or NORMAL
- **Content**: Preview of the entry text
- **Keywords**: Keywords that trigger the entry (for normal entries)

### 4. Select Entries to Import

- Each entry has a checkbox (☑ or ☐)
- Click on an entry to toggle selection
- Use **Select All** to select all visible entries
- Use **Deselect All** to deselect all entries
- Filter options update the visible entries

### 5. Choose Import Destination

**Option 1: Import to Selected Lorebook**
- Select a lorebook in the main Lorebooks tab before importing
- Choose "Selected Lorebook" in the import dialog
- Entries will be added to your existing lorebook

**Option 2: Import to New Lorebook**
- Choose "New Lorebook" in the import dialog
- Enter a name for the new lorebook
- A new lorebook will be created with the imported entries

### 6. Complete the Import

1. Click **Import** button
2. The importer will:
   - Create a new lorebook if needed
   - Add all selected entries to the target lorebook
   - Show a success message with the count of imported entries
3. The main Lorebooks tab will automatically refresh to show the changes

## Features

### ✅ Flexible Format Support
- Supports single lorebook files
- Supports config files with multiple lorebooks
- Handles lorebook arrays
- Validates JSON structure before import

### ✅ Entry Filtering
- Filter by entry type (constant/normal)
- Preview before importing
- Selective import with checkboxes

### ✅ Smart Validation
- Validates JSON structure
- Checks for required fields
- Shows clear error messages
- Prevents duplicate lorebook names

### ✅ Bulk Operations
- Import multiple entries at once
- Import from multiple lorebooks
- Select/deselect all entries quickly

### ✅ Flexible Destination
- Import to existing lorebook
- Create new lorebook during import
- Add entries to currently selected lorebook

## Example Workflow

### Scenario: Importing a Fantasy World Lorebook

1. **Prepare the File**
   - Export or create a lorebook JSON file
   - Save it as `fantasy_world.json`

2. **Open the Importer**
   - Go to Lorebooks tab
   - Click "Import..."

3. **Browse and Select**
   - Browse to `fantasy_world.json`
   - Click "Open"

4. **Preview Entries**
   - The dialog shows: "fantasy_world (5 entries)"
   - Entry list shows:
     - [CONSTANT] This is a high-fantasy medieval world...
     - [NORMAL] Dragons are powerful ancient beings... [dragon, dragons, wyrm]
     - [NORMAL] Elves are immortal forest dwellers... [elf, elves]
     - etc.

5. **Filter if Needed**
   - Want only constant entries? Select "Constant Only"
   - Want only normal entries? Select "Normal Only"

6. **Select Entries**
   - All entries are selected by default
   - Deselect any you don't want
   - Or use filters + Select All for specific types

7. **Choose Destination**
   - Option A: Select existing "my_campaign" lorebook in main window
   - Option B: Create new lorebook named "imported_fantasy"

8. **Import**
   - Click "Import"
   - Success! "Imported 5 of 5 entries to 'imported_fantasy'"

## Tips

### Creating Lorebook Files for Import

Create a JSON file with this structure:

```json
{
  "name": "my_lorebook",
  "active": true,
  "entries": [
    {
      "content": "Constant entry - always included",
      "insertion_type": "constant",
      "keywords": []
    },
    {
      "content": "Normal entry - triggered by keywords",
      "insertion_type": "normal",
      "keywords": ["keyword1", "keyword2", "keyword3"]
    }
  ]
}
```

### Best Practices

1. **Review Before Import**: Always preview entries before importing
2. **Use Filters**: Use filters to import only the entry types you need
3. **Merge vs New**: 
   - Use "Selected Lorebook" to merge with existing entries
   - Use "New Lorebook" to keep imported entries separate
4. **Backup First**: Export your current lorebooks before importing new ones
5. **Test Small First**: Test with a small lorebook before importing large ones

### Troubleshooting

**"Invalid JSON file" Error**
- Check that your file is valid JSON
- Use a JSON validator online
- Ensure all quotes and brackets are properly matched

**"Invalid lorebook format" Error**
- Ensure the file has either:
  - An "entries" field (single lorebook)
  - A "lorebooks" field (config format)
- Check that entries have required fields: content, insertion_type

**"No entries selected for import" Warning**
- Make sure at least one entry is checked (☑)
- Check if your filter is hiding all entries

**"Please select a lorebook in the main window first" Warning**
- If importing to "Selected Lorebook", click on a lorebook in the main tab first
- Or switch to "New Lorebook" mode

## Compatibility

The importer is designed to be compatible with:

- ✅ Native lorebook format (as used in this application)
- ✅ SillyTavern lorebook exports (with standard structure)
- ✅ Custom lorebook formats (with entries/insertion_type/keywords structure)
- ✅ Config backup files containing multiple lorebooks

## Technical Details

### Supported Entry Types

1. **Constant Entries**
   - `insertion_type: "constant"`
   - Always active when lorebook is active
   - No keywords required

2. **Normal Entries**
   - `insertion_type: "normal"`
   - Triggered by keywords in messages
   - Must have at least one keyword

### Field Requirements

**Required Fields:**
- `content`: The entry text
- `insertion_type`: Either "constant" or "normal"

**Optional Fields:**
- `keywords`: Array of trigger keywords (required for normal entries, empty for constant)

### Format Validation

The importer automatically detects and validates:
- JSON syntax
- Required fields presence
- Data types (arrays, strings, etc.)
- Entry type validity (constant/normal)
- Keyword presence for normal entries
