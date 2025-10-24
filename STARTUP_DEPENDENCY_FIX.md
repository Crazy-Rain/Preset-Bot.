# Startup Dependency Fix

## Problem

When running the Preset Discord Bot as a startup application (e.g., on system boot), you may encounter this error:

```
ModuleNotFoundError: No module named 'aiohttp'
```

However, when running the bot manually from a terminal, it works fine.

## Root Cause

This issue occurs because:

1. **Different Python Environments**: System startup scripts often use the system Python environment, while manual terminal sessions may use a user's Python environment with installed packages.

2. **Missing User-Installed Packages**: When dependencies are installed with `pip install --user`, they're placed in the user's home directory (`~/.local/lib/python3.x/site-packages`). System startup scripts may not have access to this location.

3. **PATH Differences**: The PATH environment variable at system startup may be different from your user session PATH.

## Solution

The bot now includes automatic dependency checking and installation in `start.py`. This fix ensures that:

1. All required dependencies are checked before the bot starts
2. Missing dependencies are automatically installed in user space
3. The correct Python interpreter and pip are used

### For Manual Running

Simply use `start.py` instead of `bot.py`:

```bash
python3 start.py
```

Then select option 2 to run the bot.

### For Startup Applications

#### Method 1: Use start.py with a wrapper (Recommended)

Create a file `run_bot.py` in your bot directory:

```python
#!/usr/bin/env python3
"""
Wrapper script for running the bot with automatic dependency management
"""
import sys
import os

# Change to bot directory
os.chdir('/path/to/Preset-Bot.')

# Ensure dependencies are available
from start import check_and_install_dependencies
if not check_and_install_dependencies():
    sys.exit(1)

# Run the bot
import bot
bot.main()
```

Make it executable:
```bash
chmod +x run_bot.py
```

Use this in your startup script:
```bash
/usr/bin/python3 /path/to/Preset-Bot./run_bot.py
```

#### Method 2: Install dependencies system-wide

Install dependencies for all users:

```bash
sudo pip3 install -r /path/to/Preset-Bot./requirements.txt
```

#### Method 3: Use a systemd service with proper environment

Create `/etc/systemd/system/preset-bot.service`:

```ini
[Unit]
Description=Preset Discord Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Preset-Bot.
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="PYTHONPATH=/home/yourusername/.local/lib/python3.x/site-packages"
ExecStart=/usr/bin/python3 /path/to/Preset-Bot./run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable preset-bot
sudo systemctl start preset-bot
```

Check status:
```bash
sudo systemctl status preset-bot
```

View logs:
```bash
journalctl -u preset-bot -f
```

## For Raspberry Pi Users

If you're using a Raspberry Pi and setting up the bot to run on startup via the desktop autostart:

Create `~/.config/autostart/preset-bot.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Preset Discord Bot
Exec=/usr/bin/python3 /home/pi/Preset-Bot./run_bot.py
```

Or use a shell script, create `~/start_preset_bot.sh`:

```bash
#!/bin/bash
cd /home/pi/Preset-Bot.
/usr/bin/python3 run_bot.py > /home/pi/preset-bot.log 2>&1
```

Make it executable:
```bash
chmod +x ~/start_preset_bot.sh
```

Then reference it in the desktop entry:
```ini
Exec=/home/pi/start_preset_bot.sh
```

## Verification

To verify the fix is working:

1. Run the test suite:
   ```bash
   python3 test_start_dependency_check.py
   ```

2. Check that all dependencies are installed:
   ```bash
   python3 -c "import discord, aiohttp, openai; print('All dependencies OK')"
   ```

3. Test the dependency check function:
   ```bash
   python3 -c "from start import check_and_install_dependencies; check_and_install_dependencies()"
   ```

## Additional Troubleshooting

### Still getting ModuleNotFoundError?

1. Check which Python is being used:
   ```bash
   which python3
   python3 --version
   ```

2. Check where modules are installed:
   ```bash
   python3 -m pip list | grep discord
   python3 -m pip list | grep aiohttp
   ```

3. Install with explicit user flag:
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

4. Check Python path:
   ```bash
   python3 -c "import sys; print('\n'.join(sys.path))"
   ```

### Permission Issues

If you get permission errors during automatic installation:

1. Make sure you have write access to `~/.local/`:
   ```bash
   ls -la ~/.local/
   ```

2. Or install dependencies manually once:
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

## Technical Details

The fix works by:

1. **Early Dependency Check**: Before importing any bot modules, `start.py` checks if all required dependencies are available
2. **Automatic Installation**: If any dependencies are missing, it automatically runs `pip install --user`
3. **Same Python Interpreter**: Uses `sys.executable` to ensure the correct Python and pip are used
4. **User Space Installation**: Uses `--user` flag to avoid permission issues
5. **Clear Error Messages**: Provides helpful messages if automatic installation fails

## Related Files

- `start.py` - Main launcher with dependency checking
- `start.sh` - Bash script with dependency checking
- `test_start_dependency_check.py` - Test suite for the fix
- `requirements.txt` - List of required dependencies
- `LAUNCH_GUIDE.md` - Comprehensive launch and troubleshooting guide
