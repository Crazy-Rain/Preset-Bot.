"""
Preset Discord Bot - Stable AI Response and Manual Send Features
"""

import json
import os
import asyncio
import aiohttp
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
                "api_key": "",
                "model": "gpt-3.5-turbo"
            },
            "thinking_tags": {
                "enabled": False,
                "start_tag": "<think>",
                "end_tag": "</think>"
            },
            "ai_config_options": {
                "max_tokens": 4096,
                "response_length": 1024,
                "temperature": 1.0,
                "top_p": 1.0,
                "reasoning_enabled": False,
                "reasoning_level": "Auto",
                "use_presence_penalty": False,
                "presence_penalty": 0.0,
                "use_frequency_penalty": False,
                "frequency_penalty": 0.0
            },
            "characters": [
                {
                    "name": "assistant",
                    "display_name": "Assistant",
                    "description": "You are a helpful assistant.",
                    "scenario": "",
                    "avatar_url": "",
                    "avatar_file": ""
                }
            ],
            "user_characters": [],
            "presets": [],
            "active_preset": None,
            "chat_history": {},
            "last_manual_send": {
                "server_id": "",
                "channel_id": ""
            }
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
                     avatar_url: str = "", avatar_file: str = "", scenario: str = "") -> None:
        """Add a new character"""
        if "characters" not in self.config:
            self.config["characters"] = []
        self.config["characters"].append({
            "name": name,
            "display_name": display_name,
            "description": description,
            "scenario": scenario,
            "avatar_url": avatar_url,
            "avatar_file": avatar_file
        })
        self.save_config()
    
    def update_character(self, index: int, name: str, display_name: str, 
                        description: str, avatar_url: str = "", avatar_file: str = "", scenario: str = "") -> None:
        """Update an existing character"""
        if "characters" in self.config and 0 <= index < len(self.config["characters"]):
            self.config["characters"][index] = {
                "name": name,
                "display_name": display_name,
                "description": description,
                "scenario": scenario,
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
    
    # User Characters Management
    def get_user_characters(self) -> list:
        """Get list of user characters"""
        return self.config.get("user_characters", [])
    
    def add_user_character(self, name: str, display_name: str, description: str,
                          avatar_url: str = "", avatar_file: str = "") -> None:
        """Add a new user character"""
        if "user_characters" not in self.config:
            self.config["user_characters"] = []
        self.config["user_characters"].append({
            "name": name,
            "display_name": display_name,
            "description": description,
            "avatar_url": avatar_url,
            "avatar_file": avatar_file
        })
        self.save_config()
    
    def update_user_character(self, index: int, name: str, display_name: str,
                             description: str, avatar_url: str = "", avatar_file: str = "") -> None:
        """Update an existing user character"""
        if "user_characters" in self.config and 0 <= index < len(self.config["user_characters"]):
            self.config["user_characters"][index] = {
                "name": name,
                "display_name": display_name,
                "description": description,
                "avatar_url": avatar_url,
                "avatar_file": avatar_file
            }
            self.save_config()
    
    def delete_user_character(self, index: int) -> None:
        """Delete a user character"""
        if "user_characters" in self.config and 0 <= index < len(self.config["user_characters"]):
            self.config["user_characters"].pop(index)
            self.save_config()
    
    def get_user_character_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a user character by name"""
        for char in self.get_user_characters():
            if char.get("name", "").lower() == name.lower():
                return char
        return None
    
    # Preset Management
    def get_presets(self) -> list:
        """Get list of presets"""
        return self.config.get("presets", [])
    
    def add_preset(self, preset_data: Dict[str, Any]) -> None:
        """Add a new preset"""
        if "presets" not in self.config:
            self.config["presets"] = []
        self.config["presets"].append(preset_data)
        self.save_config()
    
    def update_preset(self, index: int, preset_data: Dict[str, Any]) -> None:
        """Update an existing preset"""
        if "presets" in self.config and 0 <= index < len(self.config["presets"]):
            self.config["presets"][index] = preset_data
            self.save_config()
    
    def delete_preset(self, index: int) -> None:
        """Delete a preset"""
        if "presets" in self.config and 0 <= index < len(self.config["presets"]):
            self.config["presets"].pop(index)
            self.save_config()
    
    def get_preset_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a preset by name"""
        for preset in self.get_presets():
            if preset.get("name", "").lower() == name.lower():
                return preset
        return None
    
    def set_active_preset(self, preset_name: Optional[str]) -> None:
        """Set the active preset"""
        self.config["active_preset"] = preset_name
        self.save_config()
    
    def get_active_preset(self) -> Optional[Dict[str, Any]]:
        """Get the active preset"""
        active_name = self.config.get("active_preset")
        if active_name:
            return self.get_preset_by_name(active_name)
        return None
    
    # Chat History Management
    def get_chat_history(self, channel_id: str) -> list:
        """Get chat history for a channel"""
        if "chat_history" not in self.config:
            self.config["chat_history"] = {}
        return self.config["chat_history"].get(str(channel_id), [])
    
    def add_chat_message(self, channel_id: str, message_data: Dict[str, Any]) -> None:
        """Add a message to channel chat history"""
        if "chat_history" not in self.config:
            self.config["chat_history"] = {}
        channel_key = str(channel_id)
        if channel_key not in self.config["chat_history"]:
            self.config["chat_history"][channel_key] = []
        self.config["chat_history"][channel_key].append(message_data)
        self.save_config()
    
    def clear_chat_history(self, channel_id: str) -> None:
        """Clear chat history for a channel"""
        if "chat_history" in self.config:
            channel_key = str(channel_id)
            if channel_key in self.config["chat_history"]:
                self.config["chat_history"][channel_key] = []
                self.save_config()
    
    # Last Manual Send Target Management
    def get_last_manual_send_target(self) -> Dict[str, str]:
        """Get last used server and channel IDs for manual send"""
        return self.config.get("last_manual_send", {"server_id": "", "channel_id": ""})
    
    def set_last_manual_send_target(self, server_id: str, channel_id: str) -> None:
        """Save last used server and channel IDs for manual send"""
        if "last_manual_send" not in self.config:
            self.config["last_manual_send"] = {}
        self.config["last_manual_send"]["server_id"] = server_id
        self.config["last_manual_send"]["channel_id"] = channel_id
        self.save_config()
    
    # Model Management
    def get_selected_model(self) -> str:
        """Get the selected AI model"""
        return self.config.get("openai", {}).get("model", "gpt-3.5-turbo")
    
    def set_selected_model(self, model: str) -> None:
        """Set the selected AI model"""
        if "openai" not in self.config:
            self.config["openai"] = {}
        self.config["openai"]["model"] = model
        self.save_config()
    
    def get_available_models(self) -> list:
        """Get cached list of available models"""
        return self.config.get("openai", {}).get("available_models", [])
    
    # Thinking Tags Management
    def get_thinking_tags_config(self) -> Dict[str, Any]:
        """Get thinking tags configuration"""
        return self.config.get("thinking_tags", {
            "enabled": False,
            "start_tag": "<think>",
            "end_tag": "</think>"
        })
    
    def set_thinking_tags_config(self, enabled: bool, start_tag: str, end_tag: str) -> None:
        """Set thinking tags configuration"""
        if "thinking_tags" not in self.config:
            self.config["thinking_tags"] = {}
        self.config["thinking_tags"]["enabled"] = enabled
        self.config["thinking_tags"]["start_tag"] = start_tag
        self.config["thinking_tags"]["end_tag"] = end_tag
        self.save_config()
    
    # AI Configuration Options Management
    def get_ai_config_options(self) -> Dict[str, Any]:
        """Get AI configuration options"""
        return self.config.get("ai_config_options", {
            "max_tokens": 4096,
            "response_length": 1024,
            "temperature": 1.0,
            "top_p": 1.0,
            "reasoning_enabled": False,
            "reasoning_level": "Auto",
            "use_presence_penalty": False,
            "presence_penalty": 0.0,
            "use_frequency_penalty": False,
            "frequency_penalty": 0.0
        })
    
    def set_ai_config_options(self, options: Dict[str, Any]) -> None:
        """Set AI configuration options"""
        self.config["ai_config_options"] = options
        self.save_config()
    
    def remove_thinking_tags(self, text: str) -> str:
        """Remove thinking tag sections from text if enabled"""
        thinking_config = self.get_thinking_tags_config()
        
        if not thinking_config.get("enabled", False):
            return text
        
        start_tag = thinking_config.get("start_tag", "<think>")
        end_tag = thinking_config.get("end_tag", "</think>")
        
        if not start_tag or not end_tag:
            return text
        
        # Remove all occurrences of content between start_tag and end_tag
        import re
        # Use re.DOTALL to match newlines as well
        pattern = re.escape(start_tag) + r'.*?' + re.escape(end_tag)
        cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
        
        # Clean up extra whitespace
        cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)  # Remove excessive newlines
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text



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
    
    async def fetch_available_models(self) -> list:
        """Fetch available models from the API"""
        if not self.client:
            return []
        
        try:
            models_response = await asyncio.to_thread(
                self.client.models.list
            )
            models = [model.id for model in models_response.data]
            
            # Cache the models in config
            if "openai" not in self.config_manager.config:
                self.config_manager.config["openai"] = {}
            self.config_manager.config["openai"]["available_models"] = models
            self.config_manager.save_config()
            
            return models
        except Exception as e:
            print(f"Error fetching models: {str(e)}")
            return []
    
    async def get_ai_response(
        self, 
        message: str, 
        character_name: Optional[str] = None,
        model: Optional[str] = None,
        preset_override: Optional[Dict[str, Any]] = None,
        additional_context: Optional[list] = None
    ) -> str:
        """
        Get AI response for a message
        
        Args:
            message: The user message
            character_name: Name of the character to use
            model: The model to use for generation (if None, uses selected model from config)
            preset_override: Override preset configuration
            additional_context: Additional message history context
            
        Returns:
            AI generated response
        """
        if not self.client:
            return "Error: OpenAI API not configured. Please set BASE URL and API KEY."
        
        # Use selected model from config if not specified
        if model is None:
            model = self.config_manager.get_selected_model()
        
        # Get active preset or use override
        preset = preset_override or self.config_manager.get_active_preset()
        
        # Build messages array
        messages = []
        
        # Add preset blocks if available
        if preset:
            blocks = preset.get("blocks", [])
            for block in blocks:
                if block.get("active", True):
                    role = block.get("role", "system")
                    content = block.get("content", "")
                    if content:
                        messages.append({"role": role, "content": content})
        
        # Get character description as system prompt
        system_prompt = "You are a helpful assistant."
        if character_name:
            char = self.config_manager.get_character_by_name(character_name)
            if char:
                # Use description field as system prompt, fallback to system_prompt for backward compatibility
                system_prompt = char.get("description") or char.get("system_prompt", "You are a helpful assistant.")
        
        # Add character system prompt if no preset or if preset doesn't have system messages
        if not preset or not any(msg.get("role") == "system" for msg in messages):
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        # Add additional context (chat history)
        if additional_context:
            messages.extend(additional_context)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        # Get AI configuration from preset or use defaults
        ai_config = {}
        if preset:
            config = preset.get("ai_config", {})
            if config.get("max_tokens"):
                ai_config["max_tokens"] = min(config.get("max_tokens", 4096), 2000000)
            if config.get("temperature") is not None:
                ai_config["temperature"] = config.get("temperature", 1.0)
            if config.get("top_p") is not None:
                ai_config["top_p"] = config.get("top_p", 1.0)
            if config.get("presence_penalty") is not None and config.get("use_presence_penalty", False):
                ai_config["presence_penalty"] = config.get("presence_penalty", 0.0)
            if config.get("frequency_penalty") is not None and config.get("use_frequency_penalty", False):
                ai_config["frequency_penalty"] = config.get("frequency_penalty", 0.0)
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=messages,
                **ai_config
            )
            response_text = response.choices[0].message.content
            
            # Remove thinking tags if enabled
            response_text = self.config_manager.remove_thinking_tags(response_text)
            
            return response_text
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
        
        # Add event handlers
        self.add_event_handlers()
    
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
        
        @self.command(name='chat')
        async def chat(ctx, user_character: Optional[str] = None, *, message: str):
            """
            Chat using a user character - messages are tracked per channel
            Usage: !chat [user_character_name]: "dialogue" action description
            Example: !chat Alice: "Hello there!" waves enthusiastically
            """
            # Parse the message to extract dialogue and actions
            # Format: !chat CharacterName: "What is being said" What is being Done
            
            # Get user character if specified
            user_char = None
            if user_character:
                user_char = self.config_manager.get_user_character_by_name(user_character)
            
            # Build the chat message
            channel_id = str(ctx.channel.id)
            
            # Get channel chat history
            chat_history = self.config_manager.get_chat_history(channel_id)
            
            # Store this message in history
            message_data = {
                "author": str(ctx.author.id),
                "author_name": str(ctx.author.name),
                "user_character": user_character,
                "content": message,
                "type": "user",
                "timestamp": ctx.message.created_at.isoformat()
            }
            self.config_manager.add_chat_message(channel_id, message_data)
            
            # Build context from recent history (last 20 messages)
            context_messages = []
            for msg in chat_history[-20:]:
                if msg.get("type") == "user":
                    char_prefix = f"[{msg.get('user_character', msg.get('author_name'))}] " if msg.get('user_character') else f"[{msg.get('author_name')}] "
                    context_messages.append({
                        "role": "user",
                        "content": char_prefix + msg.get("content", "")
                    })
                elif msg.get("type") == "assistant":
                    context_messages.append({
                        "role": "assistant",
                        "content": msg.get("content", "")
                    })
            
            # Get AI response with context
            ai_character = self.config_manager.get_characters()[0].get("name") if self.config_manager.get_characters() else None
            response = await self.ai_handler.get_ai_response(
                message,
                character_name=ai_character,
                additional_context=context_messages
            )
            
            # Store AI response in history
            response_data = {
                "content": response,
                "type": "assistant",
                "timestamp": ctx.message.created_at.isoformat()
            }
            self.config_manager.add_chat_message(channel_id, response_data)
            
            # Send response via webhook if character is configured
            if ai_character:
                char = self.config_manager.get_character_by_name(ai_character)
                if char:
                    await self.send_via_webhook(ctx.channel, response, char)
                    return
            
            # Otherwise send normally
            await ctx.send(response)
        
        @self.command(name='clearchat')
        @commands.has_permissions(administrator=True)
        async def clear_chat(ctx):
            """Clear chat history for this channel (Admin only)"""
            channel_id = str(ctx.channel.id)
            self.config_manager.clear_chat_history(channel_id)
            await ctx.send("Chat history cleared for this channel.")
        
        @self.command(name='image')
        async def image(ctx, character_name: str, url: Optional[str] = None):
            """
            Update character avatar image
            Usage: !image <character_name> <url>
            Or: !image <character_name> (with attached image)
            Example: !image dashie https://example.com/avatar.png
            """
            try:
                # Get character
                char = self.config_manager.get_character_by_name(character_name)
                if not char:
                    await ctx.send(f"Error: Character '{character_name}' not found.")
                    return
                
                # Get character index
                characters = self.config_manager.get_characters()
                char_index = None
                for i, c in enumerate(characters):
                    if c.get("name", "").lower() == character_name.lower():
                        char_index = i
                        break
                
                if char_index is None:
                    await ctx.send(f"Error: Could not find character index for '{character_name}'.")
                    return
                
                # Check for attached image
                image_url = url
                if not image_url and ctx.message.attachments:
                    # Use first attachment
                    image_url = ctx.message.attachments[0].url
                
                if not image_url:
                    await ctx.send("Error: Please provide either a URL or attach an image to the message.")
                    return
                
                await ctx.send(f"Downloading image for '{character_name}'...")
                
                # Download the image
                avatars_dir = "character_avatars"
                os.makedirs(avatars_dir, exist_ok=True)
                
                # Determine file extension from URL
                file_ext = ".png"  # default
                if "." in image_url:
                    url_ext = image_url.split(".")[-1].split("?")[0].lower()
                    if url_ext in ["png", "jpg", "jpeg", "gif", "webp"]:
                        file_ext = f".{url_ext}"
                
                avatar_file = os.path.join(avatars_dir, f"{character_name}{file_ext}")
                
                # Download image
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status == 200:
                            with open(avatar_file, 'wb') as f:
                                f.write(await resp.read())
                        else:
                            await ctx.send(f"Error: Failed to download image (HTTP {resp.status}).")
                            return
                
                # Update character with new avatar file
                self.config_manager.update_character(
                    index=char_index,
                    name=char.get("name"),
                    display_name=char.get("display_name"),
                    description=char.get("description", ""),
                    scenario=char.get("scenario", ""),
                    avatar_url=image_url,
                    avatar_file=avatar_file
                )
                
                await ctx.send(f"✓ Avatar updated for character '{char.get('display_name', character_name)}'!")
            except Exception as e:
                await ctx.send(f"Error updating avatar: {str(e)}")
    
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
    
    def add_event_handlers(self):
        """Add event handlers for message tracking"""
        
        @self.event
        async def on_message(message):
            # Don't process bot's own messages
            if message.author == self.user:
                return
            
            # Process commands first
            await self.process_commands(message)
            
            # Track !chat messages automatically (already handled in command)
            # But we can also track webhook messages from the bot here if needed


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
