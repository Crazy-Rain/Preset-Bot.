#!/bin/bash
# Preset Bot - Quick Start Script
# This script helps launch the Preset Discord Bot easily

set -e  # Exit on error

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Print header
print_header() {
    echo ""
    echo "=================================================="
    print_message "$BLUE" "  Preset Discord Bot - Quick Start Script"
    echo "=================================================="
    echo ""
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_message "$RED" "❌ Error: Python 3 is not installed!"
        print_message "$YELLOW" "   Please install Python 3.8 or higher from https://python.org"
        exit 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    print_message "$GREEN" "✓ Python ${python_version} found"
}

# Check and install dependencies
check_dependencies() {
    if [ ! -f "requirements.txt" ]; then
        print_message "$RED" "❌ Error: requirements.txt not found!"
        exit 1
    fi
    
    print_message "$YELLOW" "📦 Checking dependencies..."
    
    # Try to import discord.py to check if dependencies are installed
    if ! python3 -c "import discord" 2>/dev/null; then
        print_message "$YELLOW" "📥 Installing dependencies..."
        # Use python3 -m pip to ensure we use the right pip for the python version
        python3 -m pip install --user -r requirements.txt
        print_message "$GREEN" "✓ Dependencies installed successfully"
    else
        print_message "$GREEN" "✓ Dependencies already installed"
    fi
}

# Check if config exists
check_config() {
    if [ ! -f "config.json" ]; then
        print_message "$YELLOW" "⚠️  Warning: config.json not found"
        print_message "$YELLOW" "   You'll need to configure the bot before first use"
        return 1
    fi
    return 0
}

# Show menu
show_menu() {
    echo ""
    echo "Please select an option:"
    echo ""
    echo "  1) Run Configuration GUI (Recommended for first-time setup)"
    echo "  2) Run Discord Bot"
    echo "  3) Check Configuration Status"
    echo "  4) Run Interactive Start Menu"
    echo "  5) Exit"
    echo ""
    echo "=================================================="
}

# Run GUI
run_gui() {
    print_message "$BLUE" "🚀 Launching Configuration GUI..."
    python3 gui.py
}

# Run bot
run_bot() {
    if ! check_config; then
        print_message "$RED" "❌ Please configure the bot first (option 1)"
        return 1
    fi
    
    print_message "$BLUE" "🚀 Starting Discord Bot..."
    print_message "$YELLOW" "   Press Ctrl+C to stop the bot"
    echo ""
    python3 bot.py
}

# Check config status
check_config_status() {
    if [ -f "validate_config.py" ]; then
        python3 validate_config.py
    elif [ -f "config.json" ]; then
        print_message "$GREEN" "✓ Configuration file exists"
        python3 -c "
import json
with open('config.json', 'r') as f:
    config = json.load(f)
discord_token = config.get('discord', {}).get('token', '')
openai_key = config.get('openai', {}).get('api_key', '')
print(f\"Discord Token: {'✓ Configured' if discord_token else '✗ Not set'}\")
print(f\"OpenAI API Key: {'✓ Configured' if openai_key else '✗ Not set'}\")
print(f\"Characters: {len(config.get('characters', []))} configured\")
"
    else
        print_message "$RED" "❌ Configuration file not found"
    fi
}

# Run interactive menu
run_interactive() {
    print_message "$BLUE" "🚀 Launching Interactive Start Menu..."
    python3 start.py
}

# Main script
main() {
    print_header
    check_python
    check_dependencies
    
    # If arguments provided, execute directly
    if [ $# -gt 0 ]; then
        case "$1" in
            gui)
                run_gui
                ;;
            bot)
                run_bot
                ;;
            check)
                check_config_status
                ;;
            interactive|menu)
                run_interactive
                ;;
            *)
                print_message "$RED" "❌ Unknown command: $1"
                echo "Usage: $0 [gui|bot|check|interactive]"
                exit 1
                ;;
        esac
        exit 0
    fi
    
    # Interactive menu
    while true; do
        show_menu
        read -p "Enter your choice (1-5): " choice
        
        case $choice in
            1)
                run_gui
                ;;
            2)
                run_bot
                ;;
            3)
                check_config_status
                ;;
            4)
                run_interactive
                ;;
            5)
                print_message "$GREEN" "👋 Goodbye!"
                exit 0
                ;;
            *)
                print_message "$RED" "❌ Invalid choice. Please enter 1-5."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main "$@"
