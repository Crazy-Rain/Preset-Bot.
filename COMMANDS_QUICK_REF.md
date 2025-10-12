# Quick Reference: New Commands

## !set - Set Your Active User Character

**Set your character manually:**
```
!set alice
```
Sets your active user character to "alice" without sending a chat message.

**What it does:**
- Sets your active character for this channel
- Character will be used when you use `!chat` without specifying a name
- Shows up when you use `!viewu`
- Persists until you change it

---

## !viewu - View Your User Character

**Without arguments** - View your current user character:
```
!viewu
```
Shows the user character you last used in `!chat` in this channel.

**With character name** - View a specific user character:
```
!viewu alice
```
Shows information about the user character named "alice".

**What you see:**
- Character display name and ID
- Avatar (if configured)
- Button to show full description

---

## !viewc - View AI Character

**Without arguments** - View channel's AI character:
```
!viewc
```
Shows the AI character responding in this channel (set via `!character`).

**With character name** - View a specific AI character:
```
!viewc narrator
```
Shows information about the AI character named "narrator".

**What you see:**
- Character display name and ID
- Scenario preview (if configured)
- Avatar (if configured)
- Button to show full description

---

## !cimage - Update User Character Avatar

**With URL:**
```
!cimage alice https://example.com/alice.png
```

**With attached image:**
```
!cimage alice
```
(Attach an image file to your Discord message)

**Supported formats:** PNG, JPG, JPEG, GIF, WEBP

**What it does:**
- Downloads and saves the image
- Updates the user character's avatar
- Image saved to `ucharacter_avatars/` directory

---

## Comparison with Similar Commands

| Command | Target | Purpose |
|---------|--------|---------|
| `!set` | User Characters | Set YOUR active character |
| `!viewu` | User Characters | View YOUR character info |
| `!viewc` | AI Characters | View CHANNEL's AI character |
| `!cimage` | User Characters | Update user character avatar |
| `!image` | AI Characters | Update AI character avatar |
| `!chat` | User Characters | Send message as your character |
| `!character` | AI Characters | Set channel's AI character |

---

## Common Workflows

### First time using a user character:
```
1. Create character in GUI (User Characters tab)
2. !cimage alice https://example.com/alice.png
3. !set alice  # Set your active character
4. !viewu  # Confirm it worked
5. !chat "Hello everyone!"  # Chat without specifying character name
```

### Alternative: Using !chat directly:
```
1. Create character in GUI (User Characters tab)
2. !cimage alice https://example.com/alice.png
3. !chat alice: "Hello everyone!"  # Sets character and sends message
4. !viewu  # Confirm it worked
```

### Quickly switch characters:
```
!set bob  # Switch to bob without sending a message
!viewu    # Verify you're now bob
```

### Check what character you're using:
```
!viewu
```

### Check what AI is responding:
```
!viewc
```

### View another user's available character:
```
!viewu bob  # Shows bob's info (anyone can view)
```

---

## Tips

✅ **Do:**
- Use `!viewu` to confirm which character you're using before important messages
- Set avatars with `!cimage` before using characters in `!chat`
- Use `!viewc` to understand the channel's AI personality

❌ **Don't:**
- Confuse `!viewu` (user characters) with `!viewc` (AI characters)
- Forget to set an avatar - it makes the character more immersive!
- Try to view a character that doesn't exist - you'll get an error

---

## Interactive Buttons

Both `!viewu` and `!viewc` show a **"Show Description"** button:
- Click it to see the full character description
- Response is private (only you see it)
- Button expires after 5 minutes

---

## Error Messages

| Message | Meaning | Solution |
|---------|---------|----------|
| "You haven't used a user character..." | No chat history | Use `!chat <character>: <msg>` first |
| "Character 'name' not found" | Character doesn't exist | Check spelling or create it in GUI |
| "Failed to download image" | URL/attachment issue | Verify URL or attach a valid image |

---

## See Full Documentation

For complete details: [NEW_COMMANDS_GUIDE.md](NEW_COMMANDS_GUIDE.md)
