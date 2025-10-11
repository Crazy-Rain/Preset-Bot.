# Lorebook Quick Reference

## Quick Commands

### Managing Lorebooks

```bash
# Create a new lorebook
!lorebook create <name>

# List all lorebooks (shows active status and entry count)
!lorebook list

# Activate/deactivate a lorebook
!lorebook activate <name>
!lorebook deactivate <name>

# Delete a lorebook
!lorebook delete <name>

# Show all entries in a lorebook
!lorebook show <name>
```

### Managing Entries

```bash
# Add a constant entry (always active)
!lorebook addentry <lorebook_name> constant "Entry content here"

# Add a normal entry with keywords
!lorebook addentry <lorebook_name> normal "Entry content" keyword1 keyword2 keyword3

# Delete an entry (use index from !lorebook show)
!lorebook delentry <lorebook_name> <entry_index>
```

## Entry Types

- **Constant**: Always sent to AI when lorebook is active
- **Normal**: Only sent when message contains one or more keywords

## Example Workflow

```bash
# 1. Create a lorebook for your world
!lorebook create fantasy_realm

# 2. Add world setting (always included)
!lorebook addentry fantasy_realm constant "This is a medieval fantasy world with magic."

# 3. Add lore about dragons (only when mentioned)
!lorebook addentry fantasy_realm normal "Dragons are wise, ancient beings." dragon dragons drake

# 4. Add lore about elves (only when mentioned)
!lorebook addentry fantasy_realm normal "Elves are immortal forest dwellers." elf elves elven

# 5. View your lorebook
!lorebook show fantasy_realm

# 6. Use in chat (dragon lore will be included)
!chat Tell me about dragons in this land

# 7. Temporarily disable lorebook
!lorebook deactivate fantasy_realm

# 8. Re-enable when needed
!lorebook activate fantasy_realm
```

## Tips

1. **Use quotes** for multi-word content: `!lorebook addentry world constant "The sky is purple"`
2. **Keywords are case-insensitive**: "Dragon" matches "dragon", "DRAGON", "dragons"
3. **Multiple keywords**: Separate with spaces: `dragon dragons drake wyrm`
4. **Check entry count**: Use `!lorebook list` to see how many entries each lorebook has
5. **View before chat**: Use `!lorebook show` to verify what will be sent to AI

## Integration

- Works with `!chat` command
- Works with `!ask` command  
- Works with channel-specific characters (`!character`)
- Works with presets (lorebook entries added after preset blocks)

## Troubleshooting

**Entry not appearing?**
- Check lorebook is active: `!lorebook list`
- Verify keywords match: Message must contain at least one keyword
- Remember: Only normal entries need keywords; constant entries always appear

**Too many entries?**
- Deactivate unused lorebooks: `!lorebook deactivate <name>`
- Delete old entries: `!lorebook delentry <name> <index>`
- Use normal entries instead of constant when possible
