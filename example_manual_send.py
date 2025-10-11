#!/usr/bin/env python3
"""
Example: Manual Send Usage

This script demonstrates how to use the manual send feature programmatically.
"""

import asyncio
from bot import ConfigManager, AIResponseHandler
import discord


async def send_manual_message(server_id: str, channel_id: str, message: str, character: str = "Assistant"):
    """
    Send a manual message to a Discord channel with AI response
    
    Args:
        server_id: Discord server (guild) ID
        channel_id: Discord channel ID  
        message: The message to send to AI
        character: Character name to use for response
    """
    # Initialize configuration and AI handler
    config_manager = ConfigManager()
    ai_handler = AIResponseHandler(config_manager)
    
    # Get AI response
    print(f"🤖 Generating AI response with character '{character}'...")
    ai_response = await ai_handler.get_ai_response(message, character)
    print(f"✓ AI Response: {ai_response[:100]}...")
    
    # Initialize Discord client
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"✓ Connected to Discord as {client.user}")
        
        try:
            # Get the channel
            channel = client.get_channel(int(channel_id))
            if not channel:
                print(f"❌ Channel {channel_id} not found")
                await client.close()
                return
            
            # Send message
            print(f"📤 Sending message to channel {channel.name}...")
            await channel.send(ai_response)
            print("✅ Message sent successfully!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        finally:
            await client.close()
    
    # Get Discord token
    token = config_manager.get_discord_token()
    if not token:
        print("❌ Discord bot token not configured!")
        print("Please configure the bot using the GUI or config.json")
        return
    
    # Run the client
    await client.start(token)


async def example_usage():
    """Example usage of manual send"""
    # Example parameters (replace with your actual values)
    SERVER_ID = "1234567890"  # Your Discord server ID
    CHANNEL_ID = "9876543210"  # Your Discord channel ID
    MESSAGE = "Write a short poem about coding"
    CHARACTER = "Assistant"
    
    print("\n" + "="*60)
    print("  Manual Send Example")
    print("="*60)
    print(f"Server ID: {SERVER_ID}")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"Message: {MESSAGE}")
    print(f"Character: {CHARACTER}")
    print("="*60 + "\n")
    
    await send_manual_message(SERVER_ID, CHANNEL_ID, MESSAGE, CHARACTER)


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Update SERVER_ID and CHANNEL_ID in this script")
    print("    before running!\n")
    
    # Uncomment the line below to run the example
    # asyncio.run(example_usage())
    
    print("Example script loaded. Edit the script to set your IDs and uncomment")
    print("the asyncio.run() line to execute the manual send.")
