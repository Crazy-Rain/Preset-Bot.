# Thinking Tags - Quick Reference

## What is it?

Automatically removes AI "internal thoughts" from responses before sending to Discord.

## Setup (30 seconds)

1. Open GUI: `python gui.py`
2. Go to **Configuration** tab
3. Find **"Thinking Tags"** section
4. ✓ Check **"Enable Thinking Tag Removal"**
5. Set **Start Tag**: `<think>` (or your model's tag)
6. Set **End Tag**: `</think>` (or your model's tag)
7. Click **"Save Configuration"**

Done! All AI responses now have thinking sections removed.

## Before & After Examples

### Example 1: Simple Case

**Before (what AI sends):**
```
<think>The user wants weather info.</think>
It's sunny today with a high of 75°F.
```

**After (what Discord sees):**
```
It's sunny today with a high of 75°F.
```

---

### Example 2: Multiple Thinking Sections

**Before:**
```
<think>Planning my response...</think>
Hello! 
<think>Should I add more details?</think>
How can I help you today?
```

**After:**
```
Hello! 
How can I help you today?
```

---

### Example 3: Multiline Thinking

**Before:**
```
<think>
Let me analyze this:
1. User asked about cats
2. I should be creative
3. Include a fun fact
</think>
Cats have been domesticated for over 4,000 years!
```

**After:**
```
Cats have been domesticated for over 4,000 years!
```

---

## Common Tag Formats

| Model/System | Start Tag | End Tag |
|--------------|-----------|---------|
| Generic | `<think>` | `</think>` |
| Alternative | `<thinking>` | `</thinking>` |
| Custom | `[INTERNAL]` | `[/INTERNAL]` |

**You can use ANY tags** - just match what your AI model uses!

---

## Quick Test

After enabling, test with this prompt in !chat:

```
!chat Tell me a joke but include <think>planning</think> in your response
```

If working correctly, you'll see the joke WITHOUT the thinking tag.

---

## Disable Anytime

1. Go to **Configuration** tab
2. ✗ Uncheck **"Enable Thinking Tag Removal"**
3. Click **"Save Configuration"**

Now thinking tags will NOT be removed (shown as-is).

---

## When to Use

✅ **Use when:**
- AI includes reasoning steps you don't want users to see
- Using models with built-in thinking (o1, Claude reasoning, etc.)
- Want cleaner, more professional responses

❌ **Don't use when:**
- You WANT to show the AI's thinking process
- Using basic models that don't include thinking tags
- Debugging AI behavior (keep tags to see reasoning)

---

## Troubleshooting

**Tags not being removed?**
- Check that feature is ✓ enabled
- Verify tags match EXACTLY (case-sensitive)
- Make sure you clicked "Save Configuration"

**Wrong content being removed?**
- Tags might be too generic (e.g., `<t>`)
- Use more specific tags (e.g., `<think>`)

---

## Advanced: Different Tags for Different Models

If using multiple models:

**Option 1:** Use tags that work for all
- Set: `<think>` / `</think>`
- Configure models to use these tags

**Option 2:** Change when switching models
- GPT-4 session: `<think>` / `</think>`
- Claude session: `<thinking>` / `</thinking>`
- Update and save before switching

---

## Configuration File

Located in `config.json`:

```json
{
  "thinking_tags": {
    "enabled": true,
    "start_tag": "<think>",
    "end_tag": "</think>"
  }
}
```

Can edit directly or use GUI.

---

## See Also

- **[THINKING_TAGS.md](THINKING_TAGS.md)** - Full documentation
- **[PRESET_FEATURES.md](PRESET_FEATURES.md)** - All features
- **[QUICKSTART_PRESETS.md](QUICKSTART_PRESETS.md)** - Getting started

---

**Version:** 2.1  
**Added:** 2025-10-11
