# Lorebook Importer - Visual Flow Guide

## Step-by-Step Visual Guide

### Step 1: Access the Importer
```
┌─────────────────────────────────────────────────────────────┐
│ Preset Discord Bot - Configuration & Manual Send             │
├─────────────────────────────────────────────────────────────┤
│ Config | Presets | Manual Send | Characters | [Lorebooks]   │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────┬─────────────────────────────────┐  │
│ │ Lorebook Management │ Entry Management                │  │
│ │                     │                                 │  │
│ │ New Lorebook: [___] │                                 │  │
│ │              [Create]                                │  │
│ │                     │                                 │  │
│ │ Lorebooks:          │                                 │  │
│ │ ┌─────────────────┐ │                                 │  │
│ │ │ ✓ Fantasy (5)   │ │                                 │  │
│ │ │ ✗ Sci-Fi (3)    │ │                                 │  │
│ │ └─────────────────┘ │                                 │  │
│ │                     │                                 │  │
│ │ [Activate] [Deactivate]                             │  │
│ │ [Delete] [Import...] [Refresh]  ← Click here!       │  │
│ └─────────────────────┴─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Browse for File
```
┌─────────────────────────────────────────┐
│ Select Lorebook JSON File               │
├─────────────────────────────────────────┤
│ Look in: [Documents         ▼]          │
│                                         │
│ ┌────────────────────────────────────┐  │
│ │ 📄 sample_lorebook.json            │  │
│ │ 📄 fantasy_world.json              │  │
│ │ 📄 sci_fi_world.json               │  │
│ │ 📁 other_files/                    │  │
│ └────────────────────────────────────┘  │
│                                         │
│ File name: [sample_lorebook.json]       │
│ File type: [JSON files (*.json)    ▼]  │
│                                         │
│              [Open]    [Cancel]         │
└─────────────────────────────────────────┘
```

### Step 3: Import Preview Dialog
```
┌───────────────────────────────────────────────────────────────────────────┐
│ Import Lorebook                                                    [X]    │
├───────────────────────────────────────────────────────────────────────────┤
│ Importing from: sample_lorebook.json                                      │
│ Found 1 lorebook(s) to import                                            │
├─────────────────────────────┬────────────────────────────────────────────┤
│ Select Lorebook to Import   │ Entry Preview                              │
│                             │                                            │
│ ┌─────────────────────────┐ │ Lorebook: imported_fantasy_world - 5 total │
│ │ imported_fantasy_world  │ │                                            │
│ │ (5 entries)            │ │ Filter Entries:                            │
│ └─────────────────────────┘ │ ⦿ All Entries  ○ Constant Only  ○ Normal  │
│                             │                                            │
│                             │ ┌────┬────────┬──────────────┬──────────┐ │
│                             │ │Imp │Type    │Content       │Keywords  │ │
│                             │ ├────┼────────┼──────────────┼──────────┤ │
│                             │ │ ☑  │CONSTANT│This is a ... │-         │ │
│                             │ │ ☑  │NORMAL  │Dragons are...│dragon... │ │
│                             │ │ ☑  │NORMAL  │Elves are ... │elf, elves│ │
│                             │ │ ☑  │NORMAL  │The Mage Gu...│mage, ... │ │
│                             │ │ ☑  │NORMAL  │Silverhaven...│silverh...│ │
│                             │ └────┴────────┴──────────────┴──────────┘ │
│                             │                                            │
│                             │ [Select All]  [Deselect All]               │
├─────────────────────────────┴────────────────────────────────────────────┤
│ Import Destination                                                        │
│ Import entries to: ○ Selected Lorebook  ⦿ New Lorebook                  │
│                    [imported_lorebook_________________________]           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                   [Import]    [Cancel]    │
└───────────────────────────────────────────────────────────────────────────┘
```

### Step 4: Filter Demonstration
```
When "Constant Only" is selected:
┌────┬────────┬──────────────┬──────────┐
│Imp │Type    │Content       │Keywords  │
├────┼────────┼──────────────┼──────────┤
│ ☑  │CONSTANT│This is a ... │-         │
└────┴────────┴──────────────┴──────────┘

When "Normal Only" is selected:
┌────┬────────┬──────────────┬──────────┐
│Imp │Type    │Content       │Keywords  │
├────┼────────┼──────────────┼──────────┤
│ ☑  │NORMAL  │Dragons are...│dragon... │
│ ☑  │NORMAL  │Elves are ... │elf, elves│
│ ☑  │NORMAL  │The Mage Gu...│mage, ... │
│ ☑  │NORMAL  │Silverhaven...│silverh...│
└────┴────────┴──────────────┴──────────┘
```

### Step 5: Selective Import
```
After clicking some entries to deselect:
┌────┬────────┬──────────────┬──────────┐
│Imp │Type    │Content       │Keywords  │
├────┼────────┼──────────────┼──────────┤
│ ☑  │CONSTANT│This is a ... │-         │  ← Will import
│ ☐  │NORMAL  │Dragons are...│dragon... │  ← Will NOT import
│ ☑  │NORMAL  │Elves are ... │elf, elves│  ← Will import
│ ☐  │NORMAL  │The Mage Gu...│mage, ... │  ← Will NOT import
│ ☑  │NORMAL  │Silverhaven...│silverh...│  ← Will import
└────┴────────┴──────────────┴──────────┘

Result: Will import 3 of 5 entries
```

### Step 6: Import Destination Options

#### Option A: Import to Selected Lorebook
```
┌────────────────────────────────────────┐
│ Import Destination                     │
│ Import entries to:                     │
│   ⦿ Selected Lorebook                 │
│   ○ New Lorebook                      │
│      [________________]                │
└────────────────────────────────────────┘

Note: Must have a lorebook selected in main window
```

#### Option B: Create New Lorebook
```
┌────────────────────────────────────────┐
│ Import Destination                     │
│ Import entries to:                     │
│   ○ Selected Lorebook                 │
│   ⦿ New Lorebook                      │
│      [my_imported_lorebook___]         │
└────────────────────────────────────────┘

Will create new lorebook with this name
```

### Step 7: Success Message
```
┌──────────────────────────────────────────┐
│             Success           [✓]        │
├──────────────────────────────────────────┤
│                                          │
│  Imported 5 of 5 entries to              │
│  'imported_lorebook'                     │
│                                          │
│                    [OK]                  │
└──────────────────────────────────────────┘
```

### Step 8: Result in Main GUI
```
┌─────────────────────────────────────────────────────────────┐
│ Lorebook Management     │ Entry Management                   │
│                         │                                    │
│ Lorebooks:              │ Selected: imported_lorebook        │
│ ┌─────────────────┐     │                                    │
│ │ ✓ Fantasy (5)   │     │ Entries in Selected Lorebook:      │
│ │ ✗ Sci-Fi (3)    │     │ ┌────────────────────────────────┐ │
│ │ ✓ imported_lor..│ ← NEW│ [C] This is a high-fantasy...  │ │
│ │   (5 entries)   │     │ │ [N] Dragons are powerful... │  │
│ └─────────────────┘     │ │     [dragon, dragons, wyrm] │  │
│                         │ │ [N] Elves are immortal...   │  │
│                         │ │     [elf, elves, elven]     │  │
│                         │ │ [N] The Mage Guild is...    │  │
│                         │ │     [mage, mages, wizard]   │  │
│                         │ │ [N] Silverhaven is the...   │  │
│                         │ │     [silverhaven, capital]  │  │
│                         │ └────────────────────────────────┘ │
└─────────────────────────┴────────────────────────────────────┘
```

## Multiple Lorebooks in File

When importing a file with multiple lorebooks:

```
┌───────────────────────────────────────────────────────────────┐
│ Import Lorebook                                               │
├───────────────────────────────────────────────────────────────┤
│ Importing from: config_backup.json                            │
│ Found 3 lorebook(s) to import                                 │
├─────────────────────────────┬─────────────────────────────────┤
│ Select Lorebook to Import   │ Entry Preview                   │
│                             │                                 │
│ ┌─────────────────────────┐ │ Select a lorebook to preview   │
│ │ fantasy_world (12)      │ │ entries                         │
│ │ sci_fi_world (8)        │ │                                 │
│ │ mystery_campaign (6)    │ │                                 │
│ └─────────────────────────┘ │                                 │
│                             │                                 │
│ Click one to preview →      │                                 │
└─────────────────────────────┴─────────────────────────────────┘
```

## Error Examples

### Invalid JSON
```
┌──────────────────────────────────────────┐
│               Error           [✗]        │
├──────────────────────────────────────────┤
│                                          │
│  Invalid JSON file:                      │
│  Expecting value: line 1 column 1 (char 0)│
│                                          │
│                    [OK]                  │
└──────────────────────────────────────────┘
```

### Invalid Format
```
┌──────────────────────────────────────────┐
│               Error           [✗]        │
├──────────────────────────────────────────┤
│                                          │
│  Invalid lorebook format:                │
│  missing 'entries' or 'lorebooks' field  │
│                                          │
│                    [OK]                  │
└──────────────────────────────────────────┘
```

### No Entries Selected
```
┌──────────────────────────────────────────┐
│              Warning          [!]        │
├──────────────────────────────────────────┤
│                                          │
│  No entries selected for import          │
│                                          │
│                    [OK]                  │
└──────────────────────────────────────────┘
```

## Key UI Elements

### Checkbox States
- ☑ = Selected (will import)
- ☐ = Not selected (will not import)

### Entry Type Labels
- [C] or CONSTANT = Always active
- [N] or NORMAL = Keyword triggered

### Status Indicators
- ✓ = Active lorebook
- ✗ = Inactive lorebook

### Interactive Elements
1. **Lorebook List**: Click to select lorebook to preview
2. **Entry Checkboxes**: Click to toggle import selection
3. **Filter Radio Buttons**: Filter entries by type
4. **Destination Radio Buttons**: Choose where to import
5. **Buttons**: Import, Cancel, Select All, Deselect All

## Workflow Summary

```
Import Button → File Browser → Load JSON → Detect Format
     ↓
Preview Dialog → Select Lorebook (if multiple)
     ↓
Apply Filters → Select Entries → Choose Destination
     ↓
Import → Validate → Add Entries → Update GUI → Success!
```

## Tips for Best Experience

1. **Preview First**: Always review entries before importing
2. **Use Filters**: Filter to import only the entry types you need
3. **Check Selection**: Verify checked entries before clicking Import
4. **Name New Books**: Give descriptive names to new lorebooks
5. **Test Small**: Try with a small file first to understand the flow

## Supported File Formats Summary

| Format | Structure | Use Case |
|--------|-----------|----------|
| Single | `{"name": "...", "entries": [...]}` | Single lorebook export |
| Config | `{"lorebooks": [...]}` | Config backup, multiple books |
| Array | `[{...}, {...}]` | Multiple lorebooks list |

All formats are auto-detected and handled appropriately!
