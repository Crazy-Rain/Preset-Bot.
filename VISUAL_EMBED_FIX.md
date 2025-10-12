# Visual Guide: Embed Description Splitting Fix

## The Problem

```
User clicks "Show Description" button
         ↓
Character has 5000 character description
         ↓
Discord API rejects: "Must be 4096 or fewer in length"
         ↓
❌ ERROR - User sees nothing
```

## The Solution

```
User clicks "Show Description" button
         ↓
Character has 5000 character description
         ↓
Check: Is length > 4096? YES
         ↓
Split using split_text_intelligently(text, max_chunk_size=4000)
         ↓
         ├─ Chunk 1: 3994 chars (ends at sentence boundary)
         ├─ Chunk 2: 1006 chars (remaining text)
         ↓
Send multiple embeds:
         ├─ Embed 1: "Description (Part 1/2)" - 3994 chars ✓
         └─ Embed 2: "Description (Part 2/2)" - 1006 chars ✓
         ↓
✅ SUCCESS - User sees complete description in 2 parts
```

## Before vs After

### Scenario: Character with 6000 character description

**BEFORE:**
```
┌─────────────────────────────────┐
│  User Character: Aria           │
│  [Show Description] Button      │
└─────────────────────────────────┘
         │ User clicks button
         ↓
┌─────────────────────────────────┐
│  ❌ ERROR                        │
│  400 Bad Request                │
│  Must be 4096 or fewer          │
└─────────────────────────────────┘
```

**AFTER:**
```
┌─────────────────────────────────┐
│  User Character: Aria           │
│  [Show Description] Button      │
└─────────────────────────────────┘
         │ User clicks button
         ↓
┌─────────────────────────────────┐
│  Description (Part 1/2)         │
│  ─────────────────────────────  │
│  Aria was born in the mystical  │
│  realm of Eldoria, a land where │
│  magic flows through every...   │
│  [3994 characters]              │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  Description (Part 2/2)         │
│  ─────────────────────────────  │
│  ...her pursuit of knowledge    │
│  and the fundamental nature of  │
│  reality.                       │
│  [2006 characters]              │
└─────────────────────────────────┘
         ↓
✅ User sees complete description!
```

## Technical Flow

```
┌────────────────────────────────────────────┐
│  show_description() button callback        │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│  description_text = self.description       │
│  or "No description available."            │
└────────────────────────────────────────────┘
                    ↓
         ┌──────────────────┐
         │ len > 4096?      │
         └──────────────────┘
            ↓           ↓
          NO           YES
            ↓            ↓
    ┌────────────┐  ┌──────────────────────────┐
    │ Send 1     │  │ chunks =                 │
    │ embed      │  │ split_text_intelligently │
    │            │  │ (text, max=4000)         │
    └────────────┘  └──────────────────────────┘
                              ↓
                    ┌──────────────────────────┐
                    │ Send first chunk as      │
                    │ interaction.response     │
                    └──────────────────────────┘
                              ↓
                    ┌──────────────────────────┐
                    │ Send remaining chunks    │
                    │ as interaction.followup  │
                    └──────────────────────────┘
```

## Commands Fixed

1. **!viewc** (View AI Character)
   - ✓ Show Description button
   - ✓ Show Scenario button

2. **!viewu** (View User Character)
   - ✓ Show Description button

## Key Points

- ✅ Limit: 4096 characters per embed description
- ✅ Chunk size: 4000 characters (96-char safety margin)
- ✅ Smart splitting: Breaks at sentence boundaries
- ✅ Seamless UX: All embeds appear instantly
- ✅ Ephemeral: Only visible to user who clicked
