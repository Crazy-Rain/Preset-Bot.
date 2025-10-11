"""
Preset Discord Bot - Stable AI Response and Manual Send Features
"""

import json
import os
import asyncio
from typing import Optional, Dict, Any
import discord
from discord.ext import commands
from openai import OpenAI


class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Create from template
            template_path = "config_template.json"
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    config = json.load(f)
                self.save_config(config)
                return config
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "discord": {
                "token": ""
            },
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "api_key": ""
            },
            "characters": [
                {
                    "name": "assistant",
                    "display_name": "Assistant",
                    "description": "You are a helpful assistant.",
                    "avatar_url": "",
                    "avatar_file": ""
                }
            ]
        }
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to file"""
        if config is not None:
            self.config = config
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_discord_token(self) -> str:
        """Get Discord bot token"""
        return self.config.get("discord", {}).get("token", "")
    
    def set_discord_token(self, token: str) -> None:
        """Set Discord bot token"""
        if "discord" not in self.config:
            self.config["discord"] = {}
        self.config["discord"]["token"] = token
        self.save_config()
    
    def get_openai_config(self) -> Dict[str, str]:
        """Get OpenAI configuration"""
        return self.config.get("openai", {})
    
    def set_openai_config(self, base_url: str, api_key: str) -> None:
        """Set OpenAI configuration"""
        self.config["openai"] = {
            "base_url": base_url,
            "api_key": api_key
        }
        self.save_config()
    
    def get_characters(self) -> list:
        """Get list of characters"""
        return self.config.get("characters", [])
    
    def add_character(self, name: str, display_name: str, description: str, 
                     avatar_url: str = "", avatar_file: str = "") -> None:
        """Add a new character"""
        if "characters" not in self.config:
            self.config["characters"] = []
        self.config["characters"].append({
            "name": name,
            "display_name": display_name,
            "description": description,
            "avatar_url": avatar_url,
            "avatar_file": avatar_file
        })
        self.save_config()
    
    def update_character(self, index: int, name: str, display_name: str, 
                        description: str, avatar_url: str = "", avatar_file: str = "") -> None:
        """Update an existing character"""
        if "characters" in self.config and 0 <= index < len(self.config["characters"]):
            self.config["characters"][index] = {
                "name": name,
                "display_name": display_name,
                "description": description,
                "avatar_url": avatar_url,
                "avatar_file": avatar_file
            }
            self.save_config()
    
    def delete_character(self, index: int) -> None:
        """Delete a character"""
        if "characters" in self.config and 0 <= index < len(self.config["characters"]):
            self.config["characters"].pop(index)
            self.save_config()
    
    def get_character_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a character by name"""
        for char in self.get_characters():
            if char.get("name", "").lower() == name.lower():
                return char
        return None


class AIResponseHandler:
    """Handles AI responses using OpenAI compatible API"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI client"""
        openai_config = self.config_manager.get_openai_config()
        base_url = openai_config.get("base_url", "https://api.openai.com/v1")
        api_key = openai_config.get("api_key", "")
        
        if api_key:
            self.client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )
    
    def update_client(self) -> None:
        """Update client with new configuration"""
        self._initialize_client()
    
    async def get_ai_response(
        self, 
        message: str, 
        character_name: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ) -> str:
        """
        Get AI response for a message
        
        Args:
            message: The user message
            character_name: Name of the character to use
            model: The model to use for generation
            
        Returns:
            AI generated response
        """
        if not self.client:
            return "Error: OpenAI API not configured. Please set BASE URL and API KEY."
        
        # Get character description as system prompt
        characters = self.config_manager.get_characters()
        system_prompt = "You are a helpful assistant."
        
        if character_name:
            char = self.config_manager.get_character_by_name(character_name)
            if char:
                # Use description field as system prompt, fallback to system_prompt for backward compatibility
                system_prompt = char.get("description") or char.get("system_prompt", "You are a helpful assistant.")
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting AI response: {str(e)}"


class PresetBot(commands.Bot):
    """Main Discord bot class"""
    
    def __init__(self, config_manager: ConfigManager):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.config_manager = config_manager
        self.ai_handler = AIResponseHandler(config_manager)
        
        # Add commands
        self.add_commands()
    
    def add_commands(self) -> None:
        """Add bot commands"""
        
        @self.command(name='settoken')
        @commands.has_permissions(administrator=True)
        async def set_token(ctx, token: str):
            """Set Discord bot token (Admin only)"""
            self.config_manager.set_discord_token(token)
            await ctx.send("Discord bot token has been updated in config.")
        
        @self.command(name='setopenai')
        @commands.has_permissions(administrator=True)
        async def set_openai(ctx, base_url: str, api_key: str):
            """Set OpenAI configuration (Admin only)"""
            self.config_manager.set_openai_config(base_url, api_key)
            self.ai_handler.update_client()
            await ctx.send(f"OpenAI configuration updated.\nBase URL: {base_url}")
        
        @self.command(name='addcharacter')
        @commands.has_permissions(administrator=True)
        async def add_character(ctx, name: str, display_name: str, *, description: str):
            """Add a new character (Admin only)"""
            self.config_manager.add_character(name, display_name, description)
            await ctx.send(f"Character '{display_name}' ({name}) has been added.")
        
        @self.command(name='characters')
        async def list_characters(ctx):
            """List all available characters"""
            characters = self.config_manager.get_characters()
            if not characters:
                await ctx.send("No characters configured.")
                return
            
            embed = discord.Embed(title="Available Characters", color=discord.Color.blue())
            for char in characters:
                display_name = char.get("display_name", char.get("name", "Unknown"))
                description = char.get("description") or char.get("system_prompt", "No description")
                embed.add_field(
                    name=f"{display_name} ({char.get('name', 'unknown')})",
                    value=description[:100] + "..." if len(description) > 100 else description,
                    inline=False
                )
            await ctx.send(embed=embed)
        
        @self.command(name='manualsend')
        @commands.has_permissions(administrator=True)
        async def manual_send(ctx, server_id: str, channel_id: str, character: str, *, message: str):
            """
            Manually send a message to a Discord channel using AI and webhooks
            Usage: !manualsend <server_id> <channel_id> <character> <message>
            """
            try:
                # Get the channel
                channel = self.get_channel(int(channel_id))
                if not channel:
                    await ctx.send(f"Error: Channel {channel_id} not found.")
                    return
                
                # Get character data
                char = self.config_manager.get_character_by_name(character)
                if not char:
                    await ctx.send(f"Error: Character '{character}' not found.")
                    return
                
                # Get AI response
                await ctx.send(f"Generating AI response with character '{char.get('display_name', character)}'...")
                ai_response = await self.ai_handler.get_ai_response(message, character)
                
                # Send via webhook
                await self.send_via_webhook(channel, ai_response, char)
                await ctx.send(f"Message sent to channel {channel.mention} as {char.get('display_name', character)}")
                
            except ValueError:
                await ctx.send("Error: Invalid server_id or channel_id. Must be numeric.")
            except Exception as e:
                await ctx.send(f"Error sending message: {str(e)}")
        
        @self.command(name='ask')
        async def ask(ctx, character: Optional[str] = None, *, message: str):
            """
            Ask the AI a question
            Usage: !ask [character] <message>
            """
            if character and character in [c.get("name") for c in self.config_manager.get_characters()]:
                response = await self.ai_handler.get_ai_response(message, character)
            else:
                # If character not found, treat it as part of the message
                full_message = f"{character} {message}" if character else message
                response = await self.ai_handler.get_ai_response(full_message)
            
            await ctx.send(response)
    
    async def send_via_webhook(self, channel, content: str, character: Dict[str, Any]) -> None:
        """
        Send a message via webhook with character identity
        
        Args:
            channel: Discord channel to send to
            content: Message content
            character: Character dictionary with display_name, avatar info
        """
        # Get or create webhook for this channel
        webhooks = await channel.webhooks()
        webhook = None
        
        # Look for existing Preset Bot webhook
        for wh in webhooks:
            if wh.name == "Preset Bot Character":
                webhook = wh
                break
        
        # Create webhook if it doesn't exist
        if not webhook:
            webhook = await channel.create_webhook(name="Preset Bot Character")
        
        # Get character display info
        display_name = character.get("display_name", character.get("name", "Character"))
        avatar_url = character.get("avatar_url", "")
        avatar_file = character.get("avatar_file", "")
        
        # If avatar_file is specified, read and use it
        avatar_bytes = None
        if avatar_file and os.path.exists(avatar_file):
            try:
                with open(avatar_file, 'rb') as f:
                    avatar_bytes = f.read()
            except Exception:
                pass
        
        # Send via webhook
        if avatar_url:
            await webhook.send(content=content, username=display_name, avatar_url=avatar_url)
        elif avatar_bytes:
            # Note: Discord webhooks don't support sending avatar as bytes in each message
            # The avatar_url parameter is required for per-message avatars
            await webhook.send(content=content, username=display_name)
        else:
            await webhook.send(content=content, username=display_name)
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')


def main():
    """Main entry point"""
    config_manager = ConfigManager()
    bot = PresetBot(config_manager)
    
    token = config_manager.get_discord_token()
    if not token:
        print("Error: Discord bot token not configured.")
        print("Please edit config.json and add your Discord bot token.")
        return
    
    bot.run(token)


if __name__ == "__main__":
    main()
