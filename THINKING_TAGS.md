# Thinking Tags Feature Documentation

## Overview

The Thinking Tags feature allows you to automatically remove AI "internal thought" sections from responses before they are sent to Discord. This is useful for models that include reasoning or thinking steps in their output that you don't want displayed to users.

## What are Thinking Tags?

Many advanced AI models (like o1, Claude with thinking, or custom fine-tuned models) include internal reasoning in their responses. This often appears within special tags:

**Example:**
```
<think>
I need to analyze this question carefully.
The user is asking about weather, so I should provide current information.
</think>
The weather today is sunny with a high of 75°F.
<think>
I should also mention tomorrow's forecast.
</think>
Tomorrow will be partly cloudy.
```

Without thinking tag removal, this entire text would be sent to Discord. With the feature enabled, only the actual response is sent:

```
The weather today is sunny with a high of 75°F.
Tomorrow will be partly cloudy.
```

## Configuration

### In the GUI

1. Open the GUI: `python gui.py`
2. Go to the **Configuration** tab
3. Scroll to the **Thinking Tags** section
4. Configure the following:
   - **Enable Thinking Tag Removal** - Check to enable the feature
   - **Start Tag** - Enter the opening tag (e.g., `<think>`, `<thinking>`, `<internal>`)
   - **End Tag** - Enter the closing tag (e.g., `</think>`, `</thinking>`, `</internal>`)
5. Click **"Save Configuration"**

### Configuration File

The settings are stored in `config.json`:

```json
{
  "thinking_tags": {
    "enabled": true,
    "start_tag": "<think>",
    "end_tag": "</think>"
  }
}
```

## Common Tag Formats

Different AI models use different formats for thinking sections:

| Model/System | Start Tag | End Tag |
|--------------|-----------|---------|
| Generic | `<think>` | `</think>` |
| Alternative 1 | `<thinking>` | `</thinking>` |
| Alternative 2 | `<internal>` | `</internal>` |
| Custom | `[THOUGHT]` | `[/THOUGHT]` |
| XML-style | `<reasoning>` | `</reasoning>` |

You can use **any** custom tags that match your AI model's format.

## How It Works

1. **AI generates response** with thinking tags
2. **Before sending to Discord**, the response is processed:
   - Regex pattern matches content between start and end tags
   - All matched sections are removed
   - Extra whitespace is cleaned up
3. **Cleaned response** is sent to Discord

### Technical Details

- Uses regex with `re.DOTALL` flag to handle multiline content
- Removes ALL occurrences (not just the first one)
- Preserves all other formatting and content
- Works with nested content within tags

## Usage Examples

### Example 1: Basic Thinking Removal

**Configuration:**
- Start Tag: `<think>`
- End Tag: `</think>`
- Enabled: ✓

**AI Response:**
```
<think>The user wants a story about cats.</think>
Once upon a time, there was a clever cat named Whiskers.
<think>I should add more details.</think>
Whiskers loved to explore the neighborhood every night.
```

**Sent to Discord:**
```
Once upon a time, there was a clever cat named Whiskers.
Whiskers loved to explore the neighborhood every night.
```

### Example 2: Different Tags

**Configuration:**
- Start Tag: `<thinking>`
- End Tag: `</thinking>`
- Enabled: ✓

**AI Response:**
```
<thinking>
Let me break this down:
1. User asked for weather
2. I should be specific
</thinking>
The temperature is 72°F with clear skies.
```

**Sent to Discord:**
```
The temperature is 72°F with clear skies.
```

### Example 3: Disabled

**Configuration:**
- Enabled: ✗

**AI Response:**
```
<think>internal reasoning</think>
Actual message.
```

**Sent to Discord:**
```
<think>internal reasoning</think>
Actual message.
```

*(When disabled, tags are NOT removed)*

## Use Cases

### 1. Role-Playing Games

AI includes strategic thinking that players shouldn't see:

```
<think>The party is low on health, so I should hint at a healing opportunity.</think>
You notice a shimmering fountain in the corner of the room.
```

Players see: `You notice a shimmering fountain in the corner of the room.`

### 2. Technical Support

AI reasons through the problem internally:

```
<think>User has a network issue. I should ask about their router first.</think>
Have you tried restarting your router? This often resolves connectivity issues.
```

User sees: `Have you tried restarting your router? This often resolves connectivity issues.`

### 3. Creative Writing

AI plans the narrative structure:

```
<think>I'll introduce a plot twist here to keep it interesting.</think>
Suddenly, the door creaked open, revealing an unexpected visitor.
```

Reader sees: `Suddenly, the door creaked open, revealing an unexpected visitor.`

## Advanced Configuration

### Multiple Models with Different Tags

If you use multiple AI models with different tag formats, you'll need to:

1. Set tags for the most commonly used model
2. OR create different presets with different configurations
3. OR manually switch tags when changing models

**Future Enhancement:** Model-specific tag configuration could be added in presets.

### Nested Tags

The current implementation handles nested tags by removing the outermost matching pairs:

```
<think>outer <think>inner</think> content</think>result
```

Result: `result`

### Special Characters in Tags

If your tags include special regex characters, they are automatically escaped, so tags like `[THINK]` or `{thought}` work correctly.

## Troubleshooting

### Tags Not Being Removed

**Check:**
1. Is the feature enabled? (checkbox checked)
2. Do the tags EXACTLY match what the AI uses?
   - Tags are case-sensitive: `<Think>` ≠ `<think>`
   - Spaces matter: `< think >` ≠ `<think>`
3. Did you save the configuration?
4. Try testing with a simple message

### Too Much Content Removed

**Issue:** Tags might match unintended content

**Solution:**
- Use more specific tags
- Example: Change `<t>` to `<think>` to avoid matching other content

### Content Still Has Extra Whitespace

The feature automatically cleans up excessive newlines, but if you notice issues:
- This is a minor formatting issue
- Extra whitespace is reduced to at most 2 newlines

## API Integration

The thinking tag removal happens in the `AIResponseHandler.get_ai_response()` method, immediately after receiving the response from the API and before returning it.

**Code Location:** `bot.py`, line ~440

```python
response_text = response.choices[0].message.content

# Remove thinking tags if enabled
response_text = self.config_manager.remove_thinking_tags(response_text)

return response_text
```

This ensures that:
- Chat history stores the cleaned version (no thinking tags)
- Discord receives the cleaned version
- The feature works consistently across all commands (!chat, !ask, etc.)

## Best Practices

1. **Test First**: Enable the feature and test with a simple message to ensure tags are correctly configured
2. **Consistent Tags**: Use the same tag format consistently in your AI prompts/system messages
3. **Document Your Tags**: If sharing presets, document which tags they expect
4. **Model-Specific**: Different models may use different formats - adjust accordingly

## Configuration File Reference

```json
{
  "thinking_tags": {
    "enabled": true,          // Boolean: Enable/disable feature
    "start_tag": "<think>",   // String: Opening tag
    "end_tag": "</think>"     // String: Closing tag
  }
}
```

## Future Enhancements

Potential improvements for future versions:

- [ ] Multiple tag pairs (e.g., remove both `<think>` and `<reasoning>`)
- [ ] Per-preset tag configuration
- [ ] Per-character tag configuration
- [ ] Option to log removed thinking to a file for debugging
- [ ] Statistics on how much content is being removed

## Related Features

- **Presets**: Configure AI behavior with message blocks
- **!chat Command**: Context-aware conversations where thinking tags are removed
- **Manual Send**: Direct messages (thinking tags not applicable since no AI)

## Version History

- **v2.1** (2025-10-11): Added thinking tags feature
  - Customizable start/end tags
  - Enable/disable toggle
  - Multiline support
  - Multiple occurrence removal

---

For more information, see:
- [PRESET_FEATURES.md](PRESET_FEATURES.md) - Complete feature documentation
- [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) - Recent changes
- [README.md](README.md) - Main documentation
