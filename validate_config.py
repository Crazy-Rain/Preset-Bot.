#!/usr/bin/env python3
"""
Configuration Validator

This script validates the bot configuration and checks for common issues.
"""

import os
import json
import sys


def load_config():
    """Load and validate config.json exists"""
    if not os.path.exists("config.json"):
        print("❌ config.json not found!")
        print("\n💡 Solutions:")
        print("   1. Run 'python gui.py' to create configuration via GUI")
        print("   2. Copy config_template.json to config.json and edit it")
        print("   3. Run the bot once to auto-create from template")
        return None
    
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return None


def validate_discord_config(config):
    """Validate Discord configuration"""
    print("\n" + "="*60)
    print("Discord Configuration")
    print("="*60)
    
    if "discord" not in config:
        print("❌ Missing 'discord' section")
        return False
    
    token = config["discord"].get("token", "")
    if not token:
        print("❌ Discord bot token is not set")
        print("\n💡 How to fix:")
        print("   1. Get token from https://discord.com/developers/applications")
        print("   2. Set it via GUI or add to config.json")
        return False
    
    if len(token) < 50:
        print("⚠️  Discord token looks too short (might be invalid)")
        print(f"   Length: {len(token)} characters")
    else:
        print(f"✅ Discord token is set ({len(token)} characters)")
    
    return True


def validate_openai_config(config):
    """Validate OpenAI configuration"""
    print("\n" + "="*60)
    print("OpenAI Configuration")
    print("="*60)
    
    if "openai" not in config:
        print("❌ Missing 'openai' section")
        return False
    
    base_url = config["openai"].get("base_url", "")
    api_key = config["openai"].get("api_key", "")
    
    # Check base URL
    if not base_url:
        print("❌ OpenAI base URL is not set")
        return False
    
    if base_url.startswith("http://") or base_url.startswith("https://"):
        print(f"✅ Base URL: {base_url}")
    else:
        print(f"⚠️  Base URL might be invalid: {base_url}")
        print("   Should start with http:// or https://")
    
    # Check API key
    if not api_key:
        print("❌ OpenAI API key is not set")
        print("\n💡 How to fix:")
        print("   1. Get API key from your OpenAI-compatible provider")
        print("   2. Set it via GUI or add to config.json")
        return False
    
    if len(api_key) < 10:
        print("⚠️  API key looks too short (might be invalid)")
        print(f"   Length: {len(api_key)} characters")
    else:
        print(f"✅ API key is set ({len(api_key)} characters)")
    
    return True


def validate_characters(config):
    """Validate characters configuration"""
    print("\n" + "="*60)
    print("Characters Configuration")
    print("="*60)
    
    if "characters" not in config:
        print("⚠️  Missing 'characters' section")
        print("   Will use defaults")
        return True
    
    characters = config["characters"]
    
    if not isinstance(characters, list):
        print("❌ 'characters' must be a list")
        return False
    
    if len(characters) == 0:
        print("⚠️  No characters configured")
        print("   Add characters via GUI or config.json")
        return True
    
    print(f"✅ {len(characters)} character(s) configured:")
    
    for i, char in enumerate(characters, 1):
        if not isinstance(char, dict):
            print(f"   ❌ Character {i}: Invalid format (must be an object)")
            continue
        
        name = char.get("name", "")
        prompt = char.get("system_prompt", "")
        
        if not name:
            print(f"   ❌ Character {i}: Missing name")
        elif not prompt:
            print(f"   ⚠️  Character {i} ({name}): Missing system_prompt")
        else:
            prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
            print(f"   ✅ {name}: {prompt_preview}")
    
    return True


def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n" + "="*60)
    print("Dependencies Check")
    print("="*60)
    
    required = ["discord", "openai"]
    all_installed = True
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n💡 Install missing packages:")
        print("   pip install -r requirements.txt")
    
    return all_installed


def print_summary(discord_ok, openai_ok, characters_ok, deps_ok):
    """Print validation summary"""
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    
    all_ok = discord_ok and openai_ok and characters_ok and deps_ok
    
    print(f"{'✅' if discord_ok else '❌'} Discord Configuration")
    print(f"{'✅' if openai_ok else '❌'} OpenAI Configuration")
    print(f"{'✅' if characters_ok else '⚠️ '} Characters Configuration")
    print(f"{'✅' if deps_ok else '❌'} Dependencies")
    
    print("="*60)
    
    if all_ok:
        print("\n🎉 Configuration is valid!")
        print("   You can now run the bot with: python bot.py")
        print("   Or use the GUI with: python gui.py")
    else:
        print("\n⚠️  Configuration has issues that need to be fixed")
        print("   See details above for how to fix each issue")
    
    return all_ok


def main():
    """Main validation function"""
    print("="*60)
    print("  Preset Bot - Configuration Validator")
    print("="*60)
    
    # Load config
    config = load_config()
    if config is None:
        return False
    
    print("✅ config.json loaded successfully")
    
    # Validate each section
    discord_ok = validate_discord_config(config)
    openai_ok = validate_openai_config(config)
    characters_ok = validate_characters(config)
    deps_ok = check_dependencies()
    
    # Print summary
    return print_summary(discord_ok, openai_ok, characters_ok, deps_ok)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Validation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
