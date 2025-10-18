# Launch Guide - Preset Discord Bot

This guide provides detailed instructions for launching the Preset Discord Bot using the new simplified methods.

## Prerequisites

- Python 3.8 or higher
- Node.js 12.0 or higher (optional, for npm commands)
- Git (for cloning the repository)

## Installation

First, clone the repository and navigate to it:

```bash
git clone https://github.com/Crazy-Rain/Preset-Bot..git
cd Preset-Bot.
```

Then install dependencies using one of these methods:

### Method 1: Using npm (Recommended)
```bash
npm install
```

This will automatically install all Python dependencies from `requirements.txt`.

### Method 2: Using pip directly
```bash
pip install -r requirements.txt
```

## Launch Methods

### 1. npm start (Easiest - Recommended for Beginners)

```bash
npm start
```

**What it does:**
- Launches an interactive menu with numbered options
- Allows you to choose between GUI, Bot, or Configuration check
- No need to remember specific commands

**Interactive Menu Options:**
1. Run Configuration GUI - Opens the graphical interface for setup
2. Run Discord Bot - Starts the bot (requires configuration)
3. Check Configuration - Validates your config.json file
4. Exit - Closes the menu

### 2. start.sh Script (Flexible Command-Line Tool)

The `start.sh` script provides both interactive and direct command modes.

#### Interactive Mode
```bash
./start.sh
```

This shows a menu similar to `npm start` with additional options.

#### Direct Commands
```bash
./start.sh gui          # Launch GUI directly
./start.sh bot          # Start the Discord bot directly
./start.sh check        # Check configuration status
./start.sh interactive  # Launch the Python interactive menu
```

**Benefits:**
- Color-coded output for better readability
- Automatic dependency checking
- Clear error messages and suggestions
- Works on Linux, macOS, and WSL

### 3. npm Scripts (For Specific Tasks)

Run specific components directly:

```bash
npm run gui             # Launch the Configuration GUI
npm run bot             # Start the Discord Bot
npm run check-config    # Validate configuration
npm test                # Run tests
```

### 4. Traditional Python Commands

You can still use the traditional Python commands:

```bash
python3 gui.py          # Launch GUI
python3 bot.py          # Start bot
python3 start.py        # Interactive menu
python3 validate_config.py  # Check config
```

## Recommended Workflow

### First-Time Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Launch the GUI to configure:**
   ```bash
   npm run gui
   ```
   Or:
   ```bash
   ./start.sh gui
   ```

3. **Configure the bot in the GUI:**
   - Enter your Discord bot token
   - Set up OpenAI API credentials
   - Add characters (optional)
   - Configure presets (optional)

4. **Start the bot:**
   ```bash
   npm run bot
   ```
   Or:
   ```bash
   ./start.sh bot
   ```

### Daily Use

For most users, the simplest approach is:

```bash
npm start
```

Then select option 2 to start the bot.

## Troubleshooting

### npm install fails

If `npm install` fails, try installing Python dependencies directly:

```bash
pip install -r requirements.txt
```

### start.sh permission denied

Make the script executable:

```bash
chmod +x start.sh
```

### Configuration file not found

The bot needs a `config.json` file. You can create it by:

1. Running the GUI: `npm run gui` or `./start.sh gui`
2. Copying the template: `cp config_template.json config.json`

### Discord bot won't start

Ensure you have:
1. Created a Discord bot in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Copied the bot token to your configuration
3. Enabled necessary intents (Message Content Intent)
4. Invited the bot to your server

## Feature Comparison

| Method | Pros | Cons |
|--------|------|------|
| `npm start` | Simplest, beginner-friendly | Requires Node.js |
| `./start.sh gui` | Fast, direct access | Requires bash shell |
| `./start.sh` | Feature-rich, color-coded | Requires bash shell |
| `npm run <command>` | Familiar to Node developers | Requires Node.js |
| `python3 <file>` | No extra dependencies | More typing required |

## Advanced Usage

### Running in Background (Linux/macOS)

To run the bot in the background:

```bash
nohup npm run bot > bot.log 2>&1 &
```

Or with start.sh:

```bash
nohup ./start.sh bot > bot.log 2>&1 &
```

To stop it:

```bash
pkill -f "python3 bot.py"
```

### Using a Virtual Environment

For isolated Python dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the bot
python3 bot.py
```

### Auto-start on System Boot (Linux)

Create a systemd service file at `/etc/systemd/system/preset-bot.service`:

```ini
[Unit]
Description=Preset Discord Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Preset-Bot.
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable preset-bot
sudo systemctl start preset-bot
```

## Summary

The new launch methods provide multiple ways to start the bot, from simple one-command launches to advanced scripted deployments. Choose the method that best fits your workflow and experience level.

For most users, we recommend:
- **First time:** `npm install` followed by `npm start`
- **Daily use:** `npm start` or `./start.sh`
- **Quick access:** `npm run gui` or `npm run bot`

Happy botting! 🤖
