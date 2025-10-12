# New Commands Documentation

This document describes the new commands added to the Preset Bot: `!viewu`, `!viewc`, and `!cimage`.

## Overview

Three new commands have been added to enhance the user experience:

1. **!viewu** - View your current user character (the one you're using in !chat)
2. **!viewc** - View the current AI/Bot character for the channel
3. **!cimage** - Update user character avatar images (similar to !image but for user characters)

---

## !viewu - View User Character

### Purpose
Shows information about your current user character - the character you're playing as when using the `!chat` command.

### Usage

```
!viewu
```
Shows your currently active user character (the last one you used in !chat in this channel)

```
!viewu <character_name>
```
Shows information about a specific user character by name

### Examples

```
!viewu
```
*Shows the user character you last used in !chat*

```
!viewu alice
```
*Shows information about the user character named "alice"*

### What It Shows

- Character Display Name
- Character ID (internal name)
- Character Avatar (as thumbnail)
- Interactive Button to view the full character description

### Features

- **Automatic Detection**: Without any arguments, `!viewu` automatically finds your last used character by checking the chat history in the current channel
- **User-Specific**: Shows YOUR character, not someone else's. Each user can have different active characters in the same channel
- **Interactive Button**: Click the "Show Description" button to see the full character description in a private message (ephemeral)
- **Avatar Display**: If the character has an avatar URL configured, it will be shown as a thumbnail in the embed

### Error Cases

- If you haven't used a user character in !chat yet: "You haven't used a user character in !chat yet in this channel."
- If you specify a character name that doesn't exist: "Error: User character 'name' not found."

---

## !viewc - View Channel Character

### Purpose
Shows information about the AI/Bot character currently set for the channel - this is the character that responds to your !chat messages.

### Usage

```
!viewc
```
Shows the current AI character for this channel

```
!viewc <character_name>
```
Shows information about a specific AI character by name

### Examples

```
!viewc
```
*Shows the AI character set for this channel, or the default character if none is set*

```
!viewc narrator
```
*Shows information about the AI character named "narrator"*

### What It Shows

- Character Display Name
- Character ID (internal name)
- Scenario (if configured) - preview of the first 100 characters
- Character Avatar (as thumbnail)
- Interactive Button to view the full character description

### Features

- **Channel-Specific**: Shows the character configured for the current channel using `!character <name>`
- **Default Fallback**: If no character is set for the channel, shows the default character (first in the list)
- **Scenario Preview**: For characters with scenarios, shows a preview in the embed
- **Interactive Button**: Click "Show Description" to see the full character description
- **Avatar Display**: If the character has an avatar URL configured, it will be shown as a thumbnail

### Error Cases

- If no characters are configured at all: "No characters configured."
- If you specify a character name that doesn't exist: "Error: Character 'name' not found."

---

## !cimage - Update User Character Avatar

### Purpose
Updates the avatar image for a user character. This is the equivalent of `!image` but specifically for user characters instead of AI characters.

### Usage

```
!cimage <character_name> <url>
```
Updates the user character's avatar using a URL

```
!cimage <character_name>
```
*(with an image attached to your Discord message)*
Updates the user character's avatar using the attached image

### Examples

```
!cimage alice https://example.com/alice_avatar.png
```
*Downloads and sets alice's avatar from the URL*

```
!cimage bob
```
*(with an image file attached to the message)*
*Uses the attached image as bob's new avatar*

### Features

- **Dual Input Methods**: Accepts either a URL or a Discord attachment
- **Automatic Download**: Downloads the image and saves it locally
- **Supported Formats**: PNG, JPG, JPEG, GIF, WEBP
- **URL Storage**: Stores both the URL and local file path in the config
- **Persistent Storage**: Images are saved in the `ucharacter_avatars/` directory

### Process

1. Bot validates that the user character exists
2. Bot downloads the image from URL or attachment
3. Image is saved to `ucharacter_avatars/<character_name>.<extension>`
4. Character config is updated with both `avatar_url` and `avatar_file`
5. Confirmation message is sent

### Error Cases

- If the character doesn't exist: "Error: User character 'name' not found."
- If no URL or attachment provided: "Error: Please provide either a URL or attach an image to the message."
- If download fails: "Error: Failed to download image (HTTP status)."

---

## Comparison: !image vs !cimage

| Feature | !image | !cimage |
|---------|--------|---------|
| Target | AI Characters | User Characters |
| Usage | `!image <char> <url>` | `!cimage <char> <url>` |
| Accepts URL | ✅ Yes | ✅ Yes |
| Accepts Attachment | ✅ Yes | ✅ Yes |
| Storage Location | `character_avatars/` | `ucharacter_avatars/` |
| Updates Field | `characters` in config | `user_characters` in config |

---

## Integration with Existing Commands

### How !viewu Works with !chat

When you use `!chat` with a user character:
```
!chat alice: "Hello there!" waves
```

The bot:
1. Records that you (your Discord User ID) used the character "alice"
2. Stores this in the channel's chat history

When you later use `!viewu` (without arguments):
1. The bot looks through the channel's chat history
2. Finds the most recent message where your User ID used a character
3. Shows you that character's information

### How !viewc Works with !character

When you use `!character` to set the channel's AI character:
```
!character narrator
```

When you later use `!viewc` (without arguments):
1. The bot checks which character is set for the current channel
2. Shows you that character's information
3. If no character is set, shows the default character (first in the list)

---

## Interactive Buttons

Both `!viewu` and `!viewc` include an interactive "Show Description" button:

- **Button Label**: "Show Description"
- **Style**: Primary (blue)
- **Timeout**: 5 minutes (300 seconds)
- **Response Type**: Ephemeral (only visible to the user who clicked)

When clicked:
1. A new embed appears with the character's full description
2. Only the user who clicked the button sees the response
3. The original message remains unchanged

---

## Use Cases

### !viewu Use Cases

1. **Check Your Active Character**: Quickly see which character you're currently playing as
2. **Reference Character Details**: View your character's description without editing config
3. **Share Character Info**: Show others what character you're using
4. **Verify Before Chat**: Confirm which character will be used before sending a !chat message

### !viewc Use Cases

1. **Check Current AI**: See which AI character is responding in the current channel
2. **Scenario Verification**: Check what scenario the AI is operating under
3. **Character Reference**: View the AI's personality/description for consistency
4. **Setup Verification**: Confirm the channel is configured correctly

### !cimage Use Cases

1. **Avatar Setup**: Add or update avatars for user characters
2. **Visual Consistency**: Ensure all user characters have appropriate avatars
3. **Character Updates**: Change a character's appearance/avatar
4. **Webhook Display**: Proper avatars ensure webhooks display correctly

---

## Technical Notes

### User Character Tracking

- User characters are tracked per Discord User ID
- Each user can have a different active character in the same channel
- Characters persist across sessions (stored in chat_history)
- History lookup goes back up to the configured `chat_history_limit` messages

### Avatar Management

- AI character avatars are stored in `character_avatars/` directory
- User character avatars are stored in `ucharacter_avatars/` directory
- Filenames follow the pattern: `<character_name>.<extension>`
- Both URL and local file paths are stored in the config
- If both exist, the URL takes precedence for webhooks

### Button Interactions

- Buttons use Discord's `discord.ui.View` and `discord.ui.Button` components
- Button responses are ephemeral (only visible to the clicker)
- Buttons automatically timeout after 5 minutes
- No special permissions required to click buttons

---

## Best Practices

1. **Set Avatars Early**: Use `!cimage` to set user character avatars before using them in !chat
2. **Verify Characters**: Use `!viewu` to verify which character is active before important !chat messages
3. **Check Channel Setup**: Use `!viewc` to ensure the channel is configured with the right AI character
4. **Use Specific Names**: When viewing a specific character, use `!viewu <name>` or `!viewc <name>` for direct access

---

## Troubleshooting

### "You haven't used a user character in !chat yet"

**Problem**: `!viewu` says you haven't used a character yet

**Solution**: Use `!chat <character_name>: <message>` at least once in the channel first

### Button Doesn't Respond

**Problem**: Clicking "Show Description" does nothing

**Solution**: The button may have timed out (5 minutes). Use the command again to get a new button.

### Character Not Found

**Problem**: `!viewu alice` says character not found

**Solution**: 
- Make sure the character exists in user_characters (check via GUI or config.json)
- Character names are case-insensitive, but must match the internal "name" field
- Use `!viewu` without arguments to see your active character instead

### No Avatar Displaying

**Problem**: Character info shows but no avatar thumbnail appears

**Solution**:
- Make sure the character has an `avatar_url` configured
- Use `!cimage <name> <url>` to set an avatar
- Verify the URL is accessible and points to a valid image
- Discord may cache images, so changes might take a moment to appear

---

## Examples & Scenarios

### Scenario 1: New User Setup

```
# Step 1: Create user character via GUI
# (Character: alice, Display Name: Alice the Brave)

# Step 2: Set avatar
!cimage alice https://example.com/alice.png

# Step 3: Use in chat
!chat alice: "I am ready for adventure!"

# Step 4: Verify
!viewu
# Shows: Alice the Brave with avatar
```

### Scenario 2: Multi-User Roleplay

```
# User1:
!chat alice: "Greetings, fellow adventurers!"
!viewu
# Shows: Alice the Brave

# User2:
!chat bob: "Well met, Alice!"
!viewu
# Shows: Bob the Wizard

# Each user sees their own character when using !viewu
```

### Scenario 3: Channel Setup

```
# Admin sets up channel
!character narrator
!viewc
# Shows: The Narrator (with scenario info)

# Users can now chat, and responses will come from "The Narrator"
```

---

## See Also

- `!chat` - Chat using a user character
- `!character` - Set the AI character for a channel
- `!image` - Update AI character avatars
- `!characters` - List all available AI characters
- Character Guide (CHARACTER_GUIDE.md)
