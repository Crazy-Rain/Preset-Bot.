#!/usr/bin/env python3
"""
Preset Bot - Quick Start Launcher
"""

import sys
import os

def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("  Preset Discord Bot - Quick Start Menu")
    print("="*50)
    print("\n1. Run Configuration GUI")
    print("2. Run Discord Bot")
    print("3. Check Configuration")
    print("4. Exit")
    print("\n" + "="*50)

def check_config():
    """Check if configuration exists"""
    if not os.path.exists("config.json"):
        print("\n❌ Configuration file not found!")
        print("   Please run the GUI (option 1) to configure the bot first.")
        return False
    
    import json
    with open("config.json", 'r') as f:
        config = json.load(f)
    
    discord_token = config.get("discord", {}).get("token", "")
    openai_key = config.get("openai", {}).get("api_key", "")
    
    print("\n" + "="*50)
    print("  Configuration Status")
    print("="*50)
    print(f"Discord Token: {'✓ Configured' if discord_token else '✗ Not set'}")
    print(f"OpenAI API Key: {'✓ Configured' if openai_key else '✗ Not set'}")
    print(f"Characters: {len(config.get('characters', []))} configured")
    print("="*50)
    
    return bool(discord_token)

def run_gui():
    """Run the GUI"""
    print("\n🚀 Launching Configuration GUI...")
    import gui
    gui.main()

def run_bot():
    """Run the Discord bot"""
    if not check_config():
        return
    
    print("\n🚀 Starting Discord Bot...")
    print("Press Ctrl+C to stop the bot\n")
    import bot
    bot.main()

def main():
    """Main entry point"""
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_gui()
        elif choice == "2":
            run_bot()
        elif choice == "3":
            check_config()
        elif choice == "4":
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
