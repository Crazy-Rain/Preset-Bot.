"""
Preset Discord Bot - Stable AI Response and Manual Send Features
"""

import json
import os
import asyncio
import aiohttp
import time
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
                "token": "",
                "reconnect": {
                    "enabled": True,
                    "max_retries": 10,
                    "base_delay": 5,
                    "max_delay": 300
                }
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
            "channel_characters": {},
            "last_manual_send": {
                "server_id": "",
                "channel_id": ""
            },
            "lorebooks": []
        }
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to file"""
        if config is not None:
            self.config = config
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def reload_config(self) -> None:
        """Reload configuration from file to get latest changes"""
        self.config = self._load_config()
    
    def get_discord_token(self) -> str:
        """Get Discord bot token"""
        return self.config.get("discord", {}).get("token", "")
    
    def get_reconnect_config(self) -> Dict[str, Any]:
        """Get reconnection configuration"""
        default_reconnect = {
            "enabled": True,
            "max_retries": 10,
            "base_delay": 5,
            "max_delay": 300
        }
        return self.config.get("discord", {}).get("reconnect", default_reconnect)
    
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
    
    # Channel Character Management
    def get_channel_character(self, channel_id: str) -> Optional[str]:
        """Get the active character for a channel"""
        if "channel_characters" not in self.config:
            self.config["channel_characters"] = {}
        return self.config["channel_characters"].get(str(channel_id))
    
    def set_channel_character(self, channel_id: str, character_name: str) -> None:
        """Set the active character for a channel"""
        if "channel_characters" not in self.config:
            self.config["channel_characters"] = {}
        self.config["channel_characters"][str(channel_id)] = character_name
        self.save_config()
    
    def clear_channel_character(self, channel_id: str) -> None:
        """Clear the active character for a channel"""
        if "channel_characters" in self.config:
            channel_key = str(channel_id)
            if channel_key in self.config["channel_characters"]:
                del self.config["channel_characters"][channel_key]
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
    
    def get_chat_history_limit(self) -> int:
        """Get chat history message limit for context"""
        return self.config.get("chat_history_limit", 20)
    
    def set_chat_history_limit(self, limit: int) -> None:
        """Set chat history message limit for context"""
        self.config["chat_history_limit"] = max(1, int(limit))  # Ensure at least 1
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


    # Lorebook Management
    def get_lorebooks(self) -> list:
        """Get list of lorebooks"""
        return self.config.get("lorebooks", [])
    
    def add_lorebook(self, name: str, active: bool = True) -> None:
        """Add a new lorebook"""
        if "lorebooks" not in self.config:
            self.config["lorebooks"] = []
        self.config["lorebooks"].append({
            "name": name,
            "active": active,
            "entries": []
        })
        self.save_config()
    
    def update_lorebook(self, index: int, name: str, active: bool) -> None:
        """Update an existing lorebook"""
        if "lorebooks" in self.config and 0 <= index < len(self.config["lorebooks"]):
            self.config["lorebooks"][index]["name"] = name
            self.config["lorebooks"][index]["active"] = active
            self.save_config()
    
    def delete_lorebook(self, index: int) -> None:
        """Delete a lorebook"""
        if "lorebooks" in self.config and 0 <= index < len(self.config["lorebooks"]):
            self.config["lorebooks"].pop(index)
            self.save_config()
    
    def get_lorebook_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a lorebook by name"""
        for lorebook in self.get_lorebooks():
            if lorebook.get("name", "").lower() == name.lower():
                return lorebook
        return None
    
    def get_lorebook_index_by_name(self, name: str) -> Optional[int]:
        """Get a lorebook index by name"""
        for i, lorebook in enumerate(self.get_lorebooks()):
            if lorebook.get("name", "").lower() == name.lower():
                return i
        return None
    
    def toggle_lorebook_active(self, name: str, active: bool) -> bool:
        """Toggle a lorebook's active state. Returns True if successful."""
        index = self.get_lorebook_index_by_name(name)
        if index is not None:
            self.config["lorebooks"][index]["active"] = active
            self.save_config()
            return True
        return False
    
    def add_lorebook_entry(self, lorebook_name: str, content: str, 
                          insertion_type: str = "normal", keywords: Optional[list] = None) -> bool:
        """
        Add an entry to a lorebook
        
        Args:
            lorebook_name: Name of the lorebook
            content: The content to be injected
            insertion_type: Either 'constant' or 'normal'
            keywords: List of keywords for normal entries (None for constant entries)
        
        Returns:
            True if successful, False otherwise
        """
        index = self.get_lorebook_index_by_name(lorebook_name)
        if index is None:
            return False
        
        if insertion_type not in ["constant", "normal"]:
            return False
        
        entry = {
            "content": content,
            "insertion_type": insertion_type,
            "keywords": keywords or []
        }
        
        self.config["lorebooks"][index]["entries"].append(entry)
        self.save_config()
        return True
    
    def update_lorebook_entry(self, lorebook_name: str, entry_index: int, 
                             content: str, insertion_type: str, keywords: Optional[list] = None) -> bool:
        """Update a lorebook entry"""
        index = self.get_lorebook_index_by_name(lorebook_name)
        if index is None:
            return False
        
        if insertion_type not in ["constant", "normal"]:
            return False
        
        lorebook = self.config["lorebooks"][index]
        if 0 <= entry_index < len(lorebook.get("entries", [])):
            lorebook["entries"][entry_index] = {
                "content": content,
                "insertion_type": insertion_type,
                "keywords": keywords or []
            }
            self.save_config()
            return True
        return False
    
    def delete_lorebook_entry(self, lorebook_name: str, entry_index: int) -> bool:
        """Delete a lorebook entry"""
        index = self.get_lorebook_index_by_name(lorebook_name)
        if index is None:
            return False
        
        lorebook = self.config["lorebooks"][index]
        if 0 <= entry_index < len(lorebook.get("entries", [])):
            lorebook["entries"].pop(entry_index)
            self.save_config()
            return True
        return False
    
    def get_active_lorebook_entries(self, message: str) -> list:
        """
        Get all relevant lorebook entries for a message.
        Returns a list of content strings to inject.
        
        Args:
            message: The user message to check against keywords
            
        Returns:
            List of entry content strings
        """
        entries = []
        message_lower = message.lower()
        
        for lorebook in self.get_lorebooks():
            lorebook_name = lorebook.get("name", "Unknown")
            is_active = lorebook.get("active", False)
            
            if not is_active:
                # Skip inactive lorebooks - they should not contribute any entries
                print(f"[Lorebook] Skipping '{lorebook_name}' - INACTIVE")
                continue
            
            print(f"[Lorebook] Processing '{lorebook_name}' - ACTIVE")
            entry_count_before = len(entries)
            
            for entry in lorebook.get("entries", []):
                insertion_type = entry.get("insertion_type", "normal")
                
                if insertion_type == "constant":
                    # Always include constant entries
                    entries.append(entry.get("content", ""))
                elif insertion_type == "normal":
                    # Check if any keyword matches
                    keywords = entry.get("keywords", [])
                    for keyword in keywords:
                        if keyword.lower() in message_lower:
                            entries.append(entry.get("content", ""))
                            break  # Don't add the same entry multiple times
            
            entries_added = len(entries) - entry_count_before
            print(f"[Lorebook] Added {entries_added} entries from '{lorebook_name}'")
        
        return entries


def split_text_intelligently(text: str, max_chunk_size: int = 1900) -> list:
    """
    Split text into chunks at sentence boundaries when possible.
    
    Args:
        text: The text to split
        max_chunk_size: Maximum size of each chunk
        
    Returns:
        List of text chunks
    """
    # If text is short enough, return as-is
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    remaining = text
    
    while remaining:
        # If what's left is small enough, add it and we're done
        if len(remaining) <= max_chunk_size:
            chunks.append(remaining)
            break
        
        # Find a good split point within the max chunk size
        chunk = remaining[:max_chunk_size]
        
        # Look for sentence endings: . ! ? followed by space or newline, or just newline
        # Search backwards from the end of the chunk
        best_split = -1
        
        # Try to find sentence boundary (. ! ? followed by space/newline or double newline)
        for i in range(len(chunk) - 1, max(len(chunk) - 200, 0), -1):
            # Check for sentence endings
            if i > 0 and chunk[i] in '.!?' and (i + 1 >= len(chunk) or chunk[i + 1] in ' \n\t'):
                best_split = i + 1
                break
            # Also check for paragraph breaks (double newline)
            if i > 0 and chunk[i-1:i+1] == '\n\n':
                best_split = i + 1
                break
        
        # If no sentence boundary found, look for any space to avoid splitting words
        if best_split == -1:
            for i in range(len(chunk) - 1, max(len(chunk) - 100, 0), -1):
                if chunk[i] == ' ':
                    best_split = i + 1
                    break
        
        # If still no good split point, just split at max_chunk_size
        if best_split == -1:
            best_split = max_chunk_size
        
        # Add the chunk and continue with the rest
        chunks.append(chunk[:best_split].rstrip())
        remaining = remaining[best_split:].lstrip()
    
    return chunks


class AIResponseHandler:
    """Handles AI responses using OpenAI compatible API"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.client = None
        self.log_callback = None
        self._initialize_client()
    
    def set_log_callback(self, callback):
        """Set a callback function for logging (e.g., to GUI console)"""
        self.log_callback = callback
    
    def _log(self, message, tag='info'):
        """Internal logging method that uses callback if available"""
        if self.log_callback:
            try:
                self.log_callback(message, tag)
            except Exception as e:
                print(f"Error in log callback: {str(e)}")
        else:
            print(message)
    
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
        additional_context: Optional[list] = None,
        user_character_info: Optional[str] = None
    ) -> str:
        """
        Get AI response for a message
        
        Args:
            message: The user message
            character_name: Name of the character to use
            model: The model to use for generation (if None, uses selected model from config)
            preset_override: Override preset configuration
            additional_context: Additional message history context
            user_character_info: User character description to add to system prompt
            
        Returns:
            AI generated response
        """
        if not self.client:
            return "Error: OpenAI API not configured. Please set BASE URL and API KEY."
        
        # Reload config to get latest lorebook/character updates from GUI or other sources
        self.config_manager.reload_config()
        
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
        
        # Add user character info to system prompt if provided
        if user_character_info:
            system_prompt += user_character_info
        
        # Add character system prompt if no preset or if preset doesn't have system messages
        if not preset or not any(msg.get("role") == "system" for msg in messages):
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        # Add lorebook entries
        lorebook_entries = self.config_manager.get_active_lorebook_entries(message)
        if lorebook_entries:
            # Combine all lorebook entries into a single system message
            lorebook_content = "\n\n".join(lorebook_entries)
            messages.append({"role": "system", "content": lorebook_content})
        
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
            # Log the request
            self._log(f"Sending AI request to model '{model}' with message: {message[:100]}...", 'request')
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=messages,
                **ai_config
            )
            response_text = response.choices[0].message.content
            
            # Remove thinking tags if enabled
            response_text = self.config_manager.remove_thinking_tags(response_text)
            
            # Log the response
            self._log(f"Received AI response: {response_text[:200]}...", 'response')
            
            return response_text
        except Exception as e:
            error_msg = f"Error getting AI response: {str(e)}"
            self._log(error_msg, 'error')
            return error_msg


class ConfigMenuView(discord.ui.View):
    """Interactive configuration menu using buttons"""
    
    def __init__(self, config_manager: ConfigManager, ai_handler: Optional['AIResponseHandler'] = None, timeout=180):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.ai_handler = ai_handler
    
    @discord.ui.button(label="🔧 OpenAI Config", style=discord.ButtonStyle.primary, row=0)
    async def openai_config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Configure OpenAI settings"""
        try:
            await interaction.response.send_modal(OpenAIConfigModal(self.config_manager, self.ai_handler))
        except Exception as e:
            await interaction.response.send_message(
                f"Error opening configuration modal: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="🤖 Characters", style=discord.ButtonStyle.primary, row=0)
    async def characters_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Manage AI characters interactively"""
        try:
            characters = self.config_manager.get_characters()
            
            embed = discord.Embed(
                title="🤖 AI Character Management",
                description="Manage your AI characters interactively below.",
                color=discord.Color.blue()
            )
            
            if characters:
                embed.add_field(
                    name="Available Characters",
                    value=f"{len(characters)} character(s) configured",
                    inline=False
                )
            else:
                embed.add_field(
                    name="No Characters",
                    value="Click 'Create Character' to get started!",
                    inline=False
                )
            
            view = CharacterManagementView(self.config_manager)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Error opening character management: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="👥 User Characters", style=discord.ButtonStyle.primary, row=0)
    async def user_characters_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Manage user characters interactively"""
        try:
            user_chars = self.config_manager.get_user_characters()
            
            embed = discord.Embed(
                title="👥 User Character Management",
                description="Manage your user/player characters interactively below.",
                color=discord.Color.green()
            )
            
            if user_chars:
                embed.add_field(
                    name="Available User Characters",
                    value=f"{len(user_chars)} character(s) configured",
                    inline=False
                )
            else:
                embed.add_field(
                    name="No User Characters",
                    value="Click 'Create User Character' to get started!",
                    inline=False
                )
            
            view = UserCharacterManagementView(self.config_manager)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Error opening user character management: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="⚙️ Bot Settings", style=discord.ButtonStyle.secondary, row=1)
    async def bot_settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """View bot settings"""
        try:
            reconnect_config = self.config_manager.get_reconnect_config()
            
            embed = discord.Embed(
                title="Bot Settings",
                description="Current bot configuration:",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="Reconnection",
                value=f"**Enabled:** {reconnect_config.get('enabled', True)}\n"
                      f"**Max Retries:** {reconnect_config.get('max_retries', 10)}\n"
                      f"**Base Delay:** {reconnect_config.get('base_delay', 5)}s\n"
                      f"**Max Delay:** {reconnect_config.get('max_delay', 300)}s",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Error viewing bot settings: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="📚 Lorebooks", style=discord.ButtonStyle.secondary, row=1)
    async def lorebooks_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Manage lorebooks interactively"""
        try:
            lorebooks = self.config_manager.get_lorebooks()
            
            embed = discord.Embed(
                title="📚 Lorebook Management",
                description="Manage your lorebooks interactively below.",
                color=discord.Color.purple()
            )
            
            if lorebooks:
                embed.add_field(
                    name="Available Lorebooks",
                    value=f"{len(lorebooks)} lorebook(s) configured",
                    inline=False
                )
            else:
                embed.add_field(
                    name="No Lorebooks",
                    value="Click 'Create Lorebook' to get started!",
                    inline=False
                )
            
            view = LorebookManagementView(self.config_manager)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            # Store the message for refresh capability
            view.message = await interaction.original_response()
        except Exception as e:
            await interaction.response.send_message(
                f"Error opening lorebook management: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="🎯 Presets", style=discord.ButtonStyle.secondary, row=1)
    async def presets_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """View presets"""
        try:
            presets = self.config_manager.get_presets()
            active_preset = self.config_manager.get_active_preset()
            
            if not presets:
                await interaction.response.send_message("No presets configured.", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="AI Presets",
                description="Available presets:",
                color=discord.Color.orange()
            )
            
            for preset in presets:
                is_active = active_preset and active_preset.get("name") == preset.get("name")
                status = "⭐ Active" if is_active else ""
                
                embed.add_field(
                    name=f"{preset.get('name', 'Unknown')} {status}",
                    value=f"Messages: {len(preset.get('messages', []))}",
                    inline=True
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Error viewing presets: {str(e)}", 
                ephemeral=True
            )
    
    @discord.ui.button(label="❌ Close", style=discord.ButtonStyle.danger, row=2)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Close the menu"""
        try:
            await interaction.response.send_message("Configuration menu closed.", ephemeral=True)
            self.stop()
        except Exception as e:
            # If response fails, try to defer and send as followup
            try:
                await interaction.followup.send(f"Menu closed with warning: {str(e)}", ephemeral=True)
            except Exception:
                pass
            self.stop()


class OpenAIConfigModal(discord.ui.Modal, title="Configure OpenAI Settings"):
    """Modal for configuring OpenAI settings"""
    
    def __init__(self, config_manager: ConfigManager, ai_handler: Optional['AIResponseHandler'] = None):
        super().__init__()
        self.config_manager = config_manager
        self.ai_handler = ai_handler
        
        # Get current config
        openai_config = config_manager.get_openai_config()
        
        # Add input fields
        self.base_url = discord.ui.TextInput(
            label="Base URL",
            placeholder="https://api.openai.com/v1",
            default=openai_config.get("base_url", "https://api.openai.com/v1"),
            required=True,
            max_length=200
        )
        self.add_item(self.base_url)
        
        self.api_key = discord.ui.TextInput(
            label="API Key",
            placeholder="sk-...",
            default=openai_config.get("api_key", ""),
            required=True,
            max_length=200,
            style=discord.TextStyle.short
        )
        self.add_item(self.api_key)
        
        self.model = discord.ui.TextInput(
            label="Model (optional)",
            placeholder="gpt-3.5-turbo",
            default=openai_config.get("model", "gpt-3.5-turbo"),
            required=False,
            max_length=100
        )
        self.add_item(self.model)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            # Update config
            openai_config = self.config_manager.get_openai_config()
            openai_config["base_url"] = self.base_url.value
            openai_config["api_key"] = self.api_key.value
            if self.model.value:
                openai_config["model"] = self.model.value
            
            self.config_manager.config["openai"] = openai_config
            self.config_manager.save_config()
            
            # Refresh the AI client with new credentials
            if self.ai_handler:
                try:
                    self.ai_handler.update_client()
                except Exception as e:
                    print(f"Error updating AI client: {str(e)}")
                    import traceback
                    print(traceback.format_exc())
            
            embed = discord.Embed(
                title="✅ OpenAI Configuration Updated",
                description="Settings have been saved successfully and client refreshed.",
                color=discord.Color.green()
            )
            embed.add_field(name="Base URL", value=self.base_url.value, inline=False)
            embed.add_field(name="API Key", value="*" * min(len(self.api_key.value), 20), inline=False)
            if self.model.value:
                embed.add_field(name="Model", value=self.model.value, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Error updating configuration: {str(e)}", 
                ephemeral=True
            )


class CreateLorebookModal(discord.ui.Modal, title="Create New Lorebook"):
    """Modal for creating a new lorebook"""
    
    def __init__(self, config_manager: ConfigManager, parent_view=None):
        super().__init__()
        self.config_manager = config_manager
        self.parent_view = parent_view
        
        self.name = discord.ui.TextInput(
            label="Lorebook Name",
            placeholder="Enter a unique name for the lorebook",
            required=True,
            max_length=50
        )
        self.add_item(self.name)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            name = self.name.value.strip()
            
            # Check if lorebook already exists
            if self.config_manager.get_lorebook_by_name(name):
                await interaction.response.send_message(
                    f"❌ Error: Lorebook '{name}' already exists.",
                    ephemeral=True
                )
                return
            
            # Create the lorebook
            self.config_manager.add_lorebook(name, active=True)
            
            embed = discord.Embed(
                title="✅ Lorebook Created",
                description=f"Lorebook '{name}' has been created and activated.",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Refresh parent view if provided
            if self.parent_view:
                await self.parent_view.refresh_view(interaction)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error creating lorebook: {str(e)}",
                ephemeral=True
            )


class AddLorebookEntryModal(discord.ui.Modal, title="Add Lorebook Entry"):
    """Modal for adding a new lorebook entry"""
    
    def __init__(self, config_manager: ConfigManager, lorebook_name: str, parent_view=None):
        super().__init__()
        self.config_manager = config_manager
        self.lorebook_name = lorebook_name
        self.parent_view = parent_view
        
        self.content = discord.ui.TextInput(
            label="Entry Content",
            placeholder="Enter the content for this entry",
            required=True,
            max_length=2000,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.content)
        
        self.entry_type = discord.ui.TextInput(
            label="Entry Type",
            placeholder="constant or normal",
            required=True,
            max_length=10,
            default="normal"
        )
        self.add_item(self.entry_type)
        
        self.keywords = discord.ui.TextInput(
            label="Keywords (for normal entries)",
            placeholder="keyword1, keyword2, keyword3",
            required=False,
            max_length=200
        )
        self.add_item(self.keywords)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            content = self.content.value.strip()
            entry_type = self.entry_type.value.strip().lower()
            
            # Validate entry type
            if entry_type not in ["constant", "normal"]:
                await interaction.response.send_message(
                    "❌ Error: Entry type must be 'constant' or 'normal'.",
                    ephemeral=True
                )
                return
            
            # Parse keywords
            keywords = []
            if entry_type == "normal" and self.keywords.value:
                keywords = [k.strip() for k in self.keywords.value.split(",") if k.strip()]
            
            # Add entry
            if self.config_manager.add_lorebook_entry(self.lorebook_name, content, entry_type, keywords):
                embed = discord.Embed(
                    title="✅ Entry Added",
                    description=f"Entry added to lorebook '{self.lorebook_name}'",
                    color=discord.Color.green()
                )
                embed.add_field(name="Type", value=entry_type.upper(), inline=True)
                if keywords:
                    embed.add_field(name="Keywords", value=", ".join(keywords), inline=True)
                embed.add_field(name="Content", value=content[:100] + "..." if len(content) > 100 else content, inline=False)
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                # Refresh parent view if provided
                if self.parent_view:
                    await self.parent_view.refresh_view(interaction)
            else:
                await interaction.response.send_message(
                    f"❌ Error: Could not add entry to lorebook '{self.lorebook_name}'.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error adding entry: {str(e)}",
                ephemeral=True
            )


class LorebookManagementView(discord.ui.View):
    """Interactive view for managing lorebooks"""
    
    def __init__(self, config_manager: ConfigManager, timeout=180):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.selected_name = None
        self.message = None
        self.update_components()
    
    def update_components(self):
        """Update the select menu with current lorebooks"""
        self.clear_items()
        
        lorebooks = self.config_manager.get_lorebooks()
        
        if lorebooks:
            # Add lorebook select menu
            options = []
            for lb in lorebooks:
                status = "✅" if lb.get("active", False) else "❌"
                entry_count = len(lb.get("entries", []))
                name = lb.get('name', 'Unknown')
                options.append(
                    discord.SelectOption(
                        label=f"{status} {name}",
                        value=name,
                        description=f"{entry_count} entries"
                    )
                )
            
            select = discord.ui.Select(
                placeholder="Select a lorebook to manage",
                options=options,
                row=0
            )
            select.callback = self.lorebook_selected
            self.add_item(select)
        
        # Add management buttons
        create_btn = discord.ui.Button(label="➕ Create Lorebook", style=discord.ButtonStyle.success, row=1)
        create_btn.callback = self.create_lorebook
        self.add_item(create_btn)
        
        if lorebooks:
            toggle_btn = discord.ui.Button(label="🔄 Toggle Active/Inactive", style=discord.ButtonStyle.primary, row=1)
            toggle_btn.callback = self.toggle_lorebook
            self.add_item(toggle_btn)
            
            add_entry_btn = discord.ui.Button(label="📝 Add Entry", style=discord.ButtonStyle.primary, row=1)
            add_entry_btn.callback = self.add_entry
            self.add_item(add_entry_btn)
            
            view_entries_btn = discord.ui.Button(label="👁️ View Entries", style=discord.ButtonStyle.secondary, row=2)
            view_entries_btn.callback = self.view_entries
            self.add_item(view_entries_btn)
            
            delete_btn = discord.ui.Button(label="🗑️ Delete Lorebook", style=discord.ButtonStyle.danger, row=2)
            delete_btn.callback = self.delete_lorebook
            self.add_item(delete_btn)
        
        close_btn = discord.ui.Button(label="❌ Close", style=discord.ButtonStyle.secondary, row=3)
        close_btn.callback = self.close
        self.add_item(close_btn)
    
    async def lorebook_selected(self, interaction: discord.Interaction):
        """Handle lorebook selection"""
        # Store the selected name for other button actions
        self.selected_name = interaction.data['values'][0]
        await interaction.response.defer()
    
    async def refresh_view(self, interaction: discord.Interaction):
        """Refresh the view to show updated lorebook list"""
        try:
            # Update components with current state
            self.update_components()
            
            # Update the original message
            lorebooks = self.config_manager.get_lorebooks()
            embed = discord.Embed(
                title="📚 Lorebook Management",
                description="Manage your lorebooks interactively below.",
                color=discord.Color.purple()
            )
            
            if lorebooks:
                embed.add_field(
                    name="Available Lorebooks",
                    value=f"{len(lorebooks)} lorebook(s) configured",
                    inline=False
                )
            else:
                embed.add_field(
                    name="No Lorebooks",
                    value="Click 'Create Lorebook' to get started!",
                    inline=False
                )
            
            if self.message:
                await self.message.edit(embed=embed, view=self)
        except Exception as e:
            print(f"Error refreshing view: {str(e)}")
    
    async def create_lorebook(self, interaction: discord.Interaction):
        """Open modal to create a new lorebook"""
        modal = CreateLorebookModal(self.config_manager, parent_view=self)
        await interaction.response.send_modal(modal)
    
    async def toggle_lorebook(self, interaction: discord.Interaction):
        """Toggle the active state of selected lorebook"""
        if not self.selected_name:
            await interaction.response.send_message(
                "⚠️ Please select a lorebook first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            lorebook = self.config_manager.get_lorebook_by_name(self.selected_name)
            if lorebook:
                current_status = lorebook.get('active', False)
                new_status = not current_status
                
                self.config_manager.toggle_lorebook_active(self.selected_name, new_status)
                
                status_text = "activated" if new_status else "deactivated"
                embed = discord.Embed(
                    title="✅ Lorebook Updated",
                    description=f"Lorebook '{self.selected_name}' has been {status_text}.",
                    color=discord.Color.green() if new_status else discord.Color.orange()
                )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                # Refresh the view to show updated status
                await self.refresh_view(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Invalid lorebook selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error toggling lorebook: {str(e)}",
                ephemeral=True
            )
    
    async def add_entry(self, interaction: discord.Interaction):
        """Open modal to add an entry to selected lorebook"""
        if not self.selected_name:
            await interaction.response.send_message(
                "⚠️ Please select a lorebook first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            lorebook = self.config_manager.get_lorebook_by_name(self.selected_name)
            if lorebook:
                modal = AddLorebookEntryModal(self.config_manager, self.selected_name, parent_view=self)
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message(
                    "❌ Invalid lorebook selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error opening add entry form: {str(e)}",
                ephemeral=True
            )
    
    async def view_entries(self, interaction: discord.Interaction):
        """View entries in the selected lorebook"""
        if not self.selected_name:
            await interaction.response.send_message(
                "⚠️ Please select a lorebook first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            lorebook = self.config_manager.get_lorebook_by_name(self.selected_name)
            if lorebook:
                name = lorebook.get('name', 'Unknown')
                entries = lorebook.get('entries', [])
                active = lorebook.get('active', False)
                
                status = "Active ✅" if active else "Inactive ❌"
                
                if not entries:
                    embed = discord.Embed(
                        title=f"📚 {name} ({status})",
                        description="This lorebook has no entries yet.",
                        color=discord.Color.blue()
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                
                embed = discord.Embed(
                    title=f"📚 {name} ({status})",
                    description=f"Total entries: {len(entries)}",
                    color=discord.Color.blue()
                )
                
                # Show first 10 entries to avoid hitting embed limits
                for i, entry in enumerate(entries[:10]):
                    entry_type = entry.get('insertion_type', 'normal').upper()
                    content = entry.get('content', '')
                    keywords = entry.get('keywords', [])
                    
                    # Truncate long content
                    if len(content) > 100:
                        content = content[:100] + "..."
                    
                    field_name = f"Entry {i} [{entry_type}]"
                    field_value = f"**Content:** {content}"
                    if entry_type == "NORMAL" and keywords:
                        field_value += f"\n**Keywords:** {', '.join(keywords[:5])}"
                    
                    embed.add_field(name=field_name, value=field_value, inline=False)
                
                if len(entries) > 10:
                    embed.set_footer(text=f"Showing 10 of {len(entries)} entries. Use !lorebook show {name} to see all.")
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid lorebook selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error viewing entries: {str(e)}",
                ephemeral=True
            )
    
    async def delete_lorebook(self, interaction: discord.Interaction):
        """Delete the selected lorebook (with confirmation)"""
        if not self.selected_name:
            await interaction.response.send_message(
                "⚠️ Please select a lorebook first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            lorebook = self.config_manager.get_lorebook_by_name(self.selected_name)
            if lorebook:
                name = lorebook.get('name', 'Unknown')
                entry_count = len(lorebook.get('entries', []))
                
                # Create confirmation view
                confirm_view = ConfirmDeleteView(self.config_manager, name, entry_count, parent_view=self)
                
                embed = discord.Embed(
                    title="⚠️ Confirm Deletion",
                    description=f"Are you sure you want to delete lorebook '{name}' with {entry_count} entries?",
                    color=discord.Color.red()
                )
                embed.set_footer(text="This action cannot be undone!")
                
                await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid lorebook selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting lorebook: {str(e)}",
                ephemeral=True
            )
    
    async def close(self, interaction: discord.Interaction):
        """Close the management view"""
        await interaction.response.send_message("Lorebook management closed.", ephemeral=True)
        self.stop()


class ConfirmDeleteView(discord.ui.View):
    """Confirmation view for deleting a lorebook"""
    
    def __init__(self, config_manager: ConfigManager, name: str, entry_count: int, parent_view=None, timeout=30):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.name = name
        self.entry_count = entry_count
        self.parent_view = parent_view
    
    @discord.ui.button(label="✅ Yes, Delete", style=discord.ButtonStyle.danger)
    async def confirm_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm deletion"""
        try:
            # Get index by name to delete
            index = self.config_manager.get_lorebook_index_by_name(self.name)
            if index is not None:
                self.config_manager.delete_lorebook(index)
                
                embed = discord.Embed(
                    title="✅ Lorebook Deleted",
                    description=f"Lorebook '{self.name}' with {self.entry_count} entries has been deleted.",
                    color=discord.Color.green()
                )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                # Refresh parent view if provided
                if self.parent_view:
                    # Clear selection since the lorebook was deleted
                    self.parent_view.selected_name = None
                    await self.parent_view.refresh_view(interaction)
                
                self.stop()
            else:
                await interaction.response.send_message(
                    f"❌ Error: Lorebook '{self.name}' not found.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting lorebook: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel deletion"""
        await interaction.response.send_message("Deletion cancelled.", ephemeral=True)
        self.stop()


class CreateCharacterModal(discord.ui.Modal, title="Create New AI Character"):
    """Modal for creating a new AI character"""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        
        self.name = discord.ui.TextInput(
            label="Character Name (internal)",
            placeholder="assistant, narrator, etc.",
            required=True,
            max_length=50
        )
        self.add_item(self.name)
        
        self.display_name = discord.ui.TextInput(
            label="Display Name",
            placeholder="The name shown in Discord",
            required=True,
            max_length=50
        )
        self.add_item(self.display_name)
        
        self.description = discord.ui.TextInput(
            label="System Prompt/Description",
            placeholder="You are a helpful assistant...",
            required=True,
            max_length=2000,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.description)
        
        self.avatar_url = discord.ui.TextInput(
            label="Avatar URL (optional)",
            placeholder="https://example.com/avatar.png",
            required=False,
            max_length=200
        )
        self.add_item(self.avatar_url)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            name = self.name.value.strip()
            display_name = self.display_name.value.strip()
            description = self.description.value.strip()
            avatar_url = self.avatar_url.value.strip() if self.avatar_url.value else ""
            
            # Check if character already exists
            if self.config_manager.get_character_by_name(name):
                await interaction.response.send_message(
                    f"❌ Error: Character '{name}' already exists.",
                    ephemeral=True
                )
                return
            
            # Create the character
            self.config_manager.add_character(name, display_name, description, avatar_url=avatar_url)
            
            embed = discord.Embed(
                title="✅ Character Created",
                description=f"AI Character '{display_name}' has been created.",
                color=discord.Color.green()
            )
            embed.add_field(name="Internal Name", value=name, inline=True)
            embed.add_field(name="Display Name", value=display_name, inline=True)
            embed.add_field(name="Description", value=description[:100] + "..." if len(description) > 100 else description, inline=False)
            if avatar_url:
                embed.add_field(name="Avatar URL", value=avatar_url, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error creating character: {str(e)}",
                ephemeral=True
            )


class CreateUserCharacterModal(discord.ui.Modal, title="Create User Character"):
    """Modal for creating a user character"""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        
        self.name = discord.ui.TextInput(
            label="Character Name (internal)",
            placeholder="john, alice, etc.",
            required=True,
            max_length=50
        )
        self.add_item(self.name)
        
        self.display_name = discord.ui.TextInput(
            label="Display Name",
            placeholder="The name shown in Discord",
            required=True,
            max_length=50
        )
        self.add_item(self.display_name)
        
        self.description = discord.ui.TextInput(
            label="Character Description",
            placeholder="A brave knight from the northern kingdom...",
            required=True,
            max_length=2000,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.description)
        
        self.avatar_url = discord.ui.TextInput(
            label="Avatar URL (optional)",
            placeholder="https://example.com/avatar.png",
            required=False,
            max_length=200
        )
        self.add_item(self.avatar_url)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            name = self.name.value.strip()
            display_name = self.display_name.value.strip()
            description = self.description.value.strip()
            avatar_url = self.avatar_url.value.strip() if self.avatar_url.value else ""
            
            # Check if character already exists
            if self.config_manager.get_user_character_by_name(name):
                await interaction.response.send_message(
                    f"❌ Error: User character '{name}' already exists.",
                    ephemeral=True
                )
                return
            
            # Create the user character
            self.config_manager.add_user_character(name, display_name, description, avatar_url=avatar_url)
            
            embed = discord.Embed(
                title="✅ User Character Created",
                description=f"User Character '{display_name}' has been created.",
                color=discord.Color.green()
            )
            embed.add_field(name="Internal Name", value=name, inline=True)
            embed.add_field(name="Display Name", value=display_name, inline=True)
            embed.add_field(name="Description", value=description[:100] + "..." if len(description) > 100 else description, inline=False)
            if avatar_url:
                embed.add_field(name="Avatar URL", value=avatar_url, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error creating user character: {str(e)}",
                ephemeral=True
            )


class CharacterManagementView(discord.ui.View):
    """Interactive view for managing AI characters"""
    
    def __init__(self, config_manager: ConfigManager, timeout=180):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.update_components()
    
    def update_components(self):
        """Update the select menu with current characters"""
        self.clear_items()
        
        characters = self.config_manager.get_characters()
        
        if characters:
            # Add character select menu
            options = []
            for i, char in enumerate(characters):
                display_name = char.get('display_name', char.get('name', 'Unknown'))
                name = char.get('name', 'N/A')
                description = char.get('description', '')[:50]
                options.append(
                    discord.SelectOption(
                        label=f"{display_name}",
                        value=str(i),
                        description=description if description else name
                    )
                )
            
            select = discord.ui.Select(
                placeholder="Select a character to view details",
                options=options,
                row=0
            )
            select.callback = self.character_selected
            self.add_item(select)
        
        # Add management buttons
        create_btn = discord.ui.Button(label="➕ Create Character", style=discord.ButtonStyle.success, row=1)
        create_btn.callback = self.create_character
        self.add_item(create_btn)
        
        if characters:
            view_btn = discord.ui.Button(label="👁️ View Details", style=discord.ButtonStyle.primary, row=1)
            view_btn.callback = self.view_character
            self.add_item(view_btn)
            
            delete_btn = discord.ui.Button(label="🗑️ Delete Character", style=discord.ButtonStyle.danger, row=1)
            delete_btn.callback = self.delete_character
            self.add_item(delete_btn)
        
        close_btn = discord.ui.Button(label="❌ Close", style=discord.ButtonStyle.secondary, row=2)
        close_btn.callback = self.close
        self.add_item(close_btn)
    
    async def character_selected(self, interaction: discord.Interaction):
        """Handle character selection"""
        self.selected_index = int(interaction.data['values'][0])
        await interaction.response.defer()
    
    async def create_character(self, interaction: discord.Interaction):
        """Open modal to create a new character"""
        await interaction.response.send_modal(CreateCharacterModal(self.config_manager))
    
    async def view_character(self, interaction: discord.Interaction):
        """View details of selected character"""
        if not hasattr(self, 'selected_index'):
            await interaction.response.send_message(
                "⚠️ Please select a character first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            characters = self.config_manager.get_characters()
            if 0 <= self.selected_index < len(characters):
                char = characters[self.selected_index]
                
                embed = discord.Embed(
                    title=f"🤖 {char.get('display_name', 'Unknown')}",
                    description=char.get('description', 'No description'),
                    color=discord.Color.blue()
                )
                embed.add_field(name="Internal Name", value=char.get('name', 'N/A'), inline=True)
                embed.add_field(name="Display Name", value=char.get('display_name', 'N/A'), inline=True)
                
                if char.get('scenario'):
                    embed.add_field(name="Scenario", value=char.get('scenario')[:200], inline=False)
                
                if char.get('avatar_url'):
                    embed.add_field(name="Avatar URL", value=char.get('avatar_url'), inline=False)
                    embed.set_thumbnail(url=char.get('avatar_url'))
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid character selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error viewing character: {str(e)}",
                ephemeral=True
            )
    
    async def delete_character(self, interaction: discord.Interaction):
        """Delete the selected character (with confirmation)"""
        if not hasattr(self, 'selected_index'):
            await interaction.response.send_message(
                "⚠️ Please select a character first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            characters = self.config_manager.get_characters()
            if 0 <= self.selected_index < len(characters):
                char = characters[self.selected_index]
                name = char.get('display_name', char.get('name', 'Unknown'))
                
                # Create confirmation view
                confirm_view = ConfirmCharacterDeleteView(self.config_manager, self.selected_index, name)
                
                embed = discord.Embed(
                    title="⚠️ Confirm Deletion",
                    description=f"Are you sure you want to delete character '{name}'?",
                    color=discord.Color.red()
                )
                embed.set_footer(text="This action cannot be undone!")
                
                await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid character selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting character: {str(e)}",
                ephemeral=True
            )
    
    async def close(self, interaction: discord.Interaction):
        """Close the management view"""
        await interaction.response.send_message("Character management closed.", ephemeral=True)
        self.stop()


class UserCharacterManagementView(discord.ui.View):
    """Interactive view for managing user characters"""
    
    def __init__(self, config_manager: ConfigManager, timeout=180):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.update_components()
    
    def update_components(self):
        """Update the select menu with current user characters"""
        self.clear_items()
        
        characters = self.config_manager.get_user_characters()
        
        if characters:
            # Add character select menu
            options = []
            for i, char in enumerate(characters):
                display_name = char.get('display_name', char.get('name', 'Unknown'))
                name = char.get('name', 'N/A')
                description = char.get('description', '')[:50]
                options.append(
                    discord.SelectOption(
                        label=f"{display_name}",
                        value=str(i),
                        description=description if description else name
                    )
                )
            
            select = discord.ui.Select(
                placeholder="Select a user character to view details",
                options=options,
                row=0
            )
            select.callback = self.character_selected
            self.add_item(select)
        
        # Add management buttons
        create_btn = discord.ui.Button(label="➕ Create User Character", style=discord.ButtonStyle.success, row=1)
        create_btn.callback = self.create_character
        self.add_item(create_btn)
        
        if characters:
            view_btn = discord.ui.Button(label="👁️ View Details", style=discord.ButtonStyle.primary, row=1)
            view_btn.callback = self.view_character
            self.add_item(view_btn)
            
            delete_btn = discord.ui.Button(label="🗑️ Delete Character", style=discord.ButtonStyle.danger, row=1)
            delete_btn.callback = self.delete_character
            self.add_item(delete_btn)
        
        close_btn = discord.ui.Button(label="❌ Close", style=discord.ButtonStyle.secondary, row=2)
        close_btn.callback = self.close
        self.add_item(close_btn)
    
    async def character_selected(self, interaction: discord.Interaction):
        """Handle character selection"""
        self.selected_index = int(interaction.data['values'][0])
        await interaction.response.defer()
    
    async def create_character(self, interaction: discord.Interaction):
        """Open modal to create a new user character"""
        await interaction.response.send_modal(CreateUserCharacterModal(self.config_manager))
    
    async def view_character(self, interaction: discord.Interaction):
        """View details of selected user character"""
        if not hasattr(self, 'selected_index'):
            await interaction.response.send_message(
                "⚠️ Please select a character first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            characters = self.config_manager.get_user_characters()
            if 0 <= self.selected_index < len(characters):
                char = characters[self.selected_index]
                
                embed = discord.Embed(
                    title=f"👥 {char.get('display_name', 'Unknown')}",
                    description=char.get('description', 'No description'),
                    color=discord.Color.green()
                )
                embed.add_field(name="Internal Name", value=char.get('name', 'N/A'), inline=True)
                embed.add_field(name="Display Name", value=char.get('display_name', 'N/A'), inline=True)
                
                if char.get('avatar_url'):
                    embed.add_field(name="Avatar URL", value=char.get('avatar_url'), inline=False)
                    embed.set_thumbnail(url=char.get('avatar_url'))
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid character selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error viewing character: {str(e)}",
                ephemeral=True
            )
    
    async def delete_character(self, interaction: discord.Interaction):
        """Delete the selected user character (with confirmation)"""
        if not hasattr(self, 'selected_index'):
            await interaction.response.send_message(
                "⚠️ Please select a character first using the dropdown menu.",
                ephemeral=True
            )
            return
        
        try:
            characters = self.config_manager.get_user_characters()
            if 0 <= self.selected_index < len(characters):
                char = characters[self.selected_index]
                name = char.get('display_name', char.get('name', 'Unknown'))
                
                # Create confirmation view
                confirm_view = ConfirmUserCharacterDeleteView(self.config_manager, self.selected_index, name)
                
                embed = discord.Embed(
                    title="⚠️ Confirm Deletion",
                    description=f"Are you sure you want to delete user character '{name}'?",
                    color=discord.Color.red()
                )
                embed.set_footer(text="This action cannot be undone!")
                
                await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Invalid character selection.",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting character: {str(e)}",
                ephemeral=True
            )
    
    async def close(self, interaction: discord.Interaction):
        """Close the management view"""
        await interaction.response.send_message("User character management closed.", ephemeral=True)
        self.stop()


class ConfirmCharacterDeleteView(discord.ui.View):
    """Confirmation view for deleting an AI character"""
    
    def __init__(self, config_manager: ConfigManager, index: int, name: str, timeout=30):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.index = index
        self.name = name
    
    @discord.ui.button(label="✅ Yes, Delete", style=discord.ButtonStyle.danger)
    async def confirm_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm deletion"""
        try:
            self.config_manager.delete_character(self.index)
            
            embed = discord.Embed(
                title="✅ Character Deleted",
                description=f"Character '{self.name}' has been deleted.",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            self.stop()
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting character: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel deletion"""
        await interaction.response.send_message("Deletion cancelled.", ephemeral=True)
        self.stop()


class ConfirmUserCharacterDeleteView(discord.ui.View):
    """Confirmation view for deleting a user character"""
    
    def __init__(self, config_manager: ConfigManager, index: int, name: str, timeout=30):
        super().__init__(timeout=timeout)
        self.config_manager = config_manager
        self.index = index
        self.name = name
    
    @discord.ui.button(label="✅ Yes, Delete", style=discord.ButtonStyle.danger)
    async def confirm_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm deletion"""
        try:
            self.config_manager.delete_user_character(self.index)
            
            embed = discord.Embed(
                title="✅ User Character Deleted",
                description=f"User character '{self.name}' has been deleted.",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            self.stop()
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error deleting user character: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel deletion"""
        await interaction.response.send_message("Deletion cancelled.", ephemeral=True)
        self.stop()


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
                # Reload config to get latest character/lorebook updates
                self.config_manager.reload_config()
                
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
            # Reload config to get latest character/lorebook updates
            self.config_manager.reload_config()
            
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
            try:
                # Validate that message is not empty or only whitespace
                if not message or not message.strip():
                    await ctx.send("Please provide a message. Usage: `!chat [character]: your message here`")
                    return
                
                # Reload config to get latest character/lorebook updates
                self.config_manager.reload_config()
                
                # Parse the message to extract dialogue and actions
                # Format: !chat CharacterName: "What is being said" What is being Done
                
                # Get user character if specified, or use the last user character from this channel
                user_char = None
                user_char_info = ""
                active_user_character = user_character
                
                # Build the chat message
                channel_id = str(ctx.channel.id)
                
                # Get chat history limit from config
                history_limit = self.config_manager.get_chat_history_limit()
                
                # If no user character specified, check if one was used recently in this channel
                if not active_user_character:
                    chat_history = self.config_manager.get_chat_history(channel_id)
                    # Look through recent history for a user character
                    for msg in reversed(chat_history[-history_limit:]):
                        if msg.get("user_character") and msg.get("author") == str(ctx.author.id):
                            active_user_character = msg.get("user_character")
                            break
                
                # Get user character info if we have an active character
                if active_user_character:
                    user_char = self.config_manager.get_user_character_by_name(active_user_character)
                    if user_char:
                        # Build persona information from user character
                        user_char_info = f"\n\nUser is playing as {user_char.get('display_name', active_user_character)}."
                        if user_char.get('description'):
                            user_char_info += f"\nCharacter description: {user_char.get('description')}"
                
                # Get channel chat history
                chat_history = self.config_manager.get_chat_history(channel_id)
                
                # Store this message in history
                message_data = {
                    "author": str(ctx.author.id),
                    "author_name": str(ctx.author.name),
                    "user_character": active_user_character,  # Store the active character (may be inherited)
                    "content": message,
                    "type": "user",
                    "timestamp": ctx.message.created_at.isoformat()
                }
                self.config_manager.add_chat_message(channel_id, message_data)
                
                # Build context from recent history (using configured limit)
                context_messages = []
                for msg in chat_history[-history_limit:]:
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
                # Use channel-specific character if set, otherwise use first character
                channel_id = str(ctx.channel.id)
                ai_character = self.config_manager.get_channel_character(channel_id)
                if not ai_character and self.config_manager.get_characters():
                    ai_character = self.config_manager.get_characters()[0].get("name")
                
                # Pass user character info to AI handler to be included in system prompt
                response = await self.ai_handler.get_ai_response(
                    message,
                    character_name=ai_character,
                    additional_context=context_messages,
                    user_character_info=user_char_info if user_char_info else None
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
            except Exception as e:
                error_msg = f"Error in chat command: {str(e)}"
                print(error_msg)
                import traceback
                print(traceback.format_exc())
                await ctx.send(f"An error occurred while processing your chat message: {str(e)}")
        
        @self.command(name='clearchat')
        @commands.has_permissions(administrator=True)
        async def clear_chat(ctx):
            """Clear chat history for this channel (Admin only)"""
            channel_id = str(ctx.channel.id)
            self.config_manager.clear_chat_history(channel_id)
            await ctx.send("Chat history cleared for this channel.")
        
        @self.command(name='character')
        async def set_character(ctx, character_name: Optional[str] = None):
            """
            Set which character the bot responds as in this channel
            Usage: !character <character_name>
            Usage: !character (with no name to clear)
            Example: !character dashie
            """
            channel_id = str(ctx.channel.id)
            
            if not character_name:
                # Clear the channel character
                self.config_manager.clear_channel_character(channel_id)
                await ctx.send("Channel character cleared. Bot will use default character.")
                return
            
            # Check if character exists
            char = self.config_manager.get_character_by_name(character_name)
            if not char:
                await ctx.send(f"Error: Character '{character_name}' not found. Use !characters to see available characters.")
                return
            
            # Set the channel character
            self.config_manager.set_channel_character(channel_id, character_name)
            await ctx.send(f"✓ Channel character set to '{char.get('display_name', character_name)}'. All responses in this channel will use this character.")
        
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
        
        @self.command(name='cimage')
        async def cimage(ctx, character_name: str, url: Optional[str] = None):
            """
            Update user character avatar image
            Usage: !cimage <character_name> <url>
            Or: !cimage <character_name> (with attached image)
            Example: !cimage Alice https://example.com/avatar.png
            """
            try:
                # Get user character
                char = self.config_manager.get_user_character_by_name(character_name)
                if not char:
                    await ctx.send(f"Error: User character '{character_name}' not found.")
                    return
                
                # Get user character index
                user_characters = self.config_manager.get_user_characters()
                char_index = None
                for i, c in enumerate(user_characters):
                    if c.get("name", "").lower() == character_name.lower():
                        char_index = i
                        break
                
                if char_index is None:
                    await ctx.send(f"Error: Could not find user character index for '{character_name}'.")
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
                avatars_dir = "ucharacter_avatars"
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
                
                # Update user character with new avatar file
                self.config_manager.update_user_character(
                    index=char_index,
                    name=char.get("name"),
                    display_name=char.get("display_name"),
                    description=char.get("description", ""),
                    avatar_url=image_url,
                    avatar_file=avatar_file
                )
                
                await ctx.send(f"✓ Avatar updated for user character '{char.get('display_name', character_name)}'!")
            except Exception as e:
                await ctx.send(f"Error updating avatar: {str(e)}")
        
        @self.command(name='viewu')
        async def viewu(ctx, user_character_name: Optional[str] = None):
            """
            View your current user character (the one you're using in !chat)
            Usage: !viewu
            Or: !viewu <character_name> to view a specific user character
            """
            try:
                # If a specific character name is provided, show that character
                if user_character_name:
                    user_char = self.config_manager.get_user_character_by_name(user_character_name)
                    if not user_char:
                        await ctx.send(f"Error: User character '{user_character_name}' not found.")
                        return
                else:
                    # Find the user's active character by looking through chat history
                    channel_id = str(ctx.channel.id)
                    chat_history = self.config_manager.get_chat_history(channel_id)
                    history_limit = self.config_manager.get_chat_history_limit()
                    
                    active_user_character = None
                    # Look through recent history for this user's character
                    for msg in reversed(chat_history[-history_limit:]):
                        if msg.get("user_character") and msg.get("author") == str(ctx.author.id):
                            active_user_character = msg.get("user_character")
                            break
                    
                    if not active_user_character:
                        await ctx.send("You haven't used a user character in !chat yet in this channel.")
                        return
                    
                    user_char = self.config_manager.get_user_character_by_name(active_user_character)
                    if not user_char:
                        await ctx.send(f"Error: Your active user character '{active_user_character}' was not found in the config.")
                        return
                
                # Create an embed to display the character info
                embed = discord.Embed(
                    title=f"User Character: {user_char.get('display_name', user_char.get('name', 'Unknown'))}",
                    color=discord.Color.green()
                )
                
                embed.add_field(name="Character ID", value=user_char.get("name", "Unknown"), inline=False)
                
                # Add avatar if available
                avatar_url = user_char.get("avatar_url", "")
                if avatar_url:
                    embed.set_thumbnail(url=avatar_url)
                
                # Create a view with a button to show description
                class DescriptionView(discord.ui.View):
                    def __init__(self, description, avatar_url, avatar_file):
                        super().__init__(timeout=300)  # 5 minute timeout
                        self.description = description
                        self.avatar_url = avatar_url
                        self.avatar_file = avatar_file
                    
                    @discord.ui.button(label="Show Description", style=discord.ButtonStyle.primary)
                    async def show_description(self, interaction: discord.Interaction, button: discord.ui.Button):
                        description_text = self.description if self.description else "No description available."
                        
                        # Send avatar image first if available
                        if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                            avatar_embed = discord.Embed(
                                title="Avatar",
                                color=discord.Color.blue()
                            )
                            
                            # Set the image in the embed
                            if self.avatar_url:
                                avatar_embed.set_image(url=self.avatar_url)
                            
                            # Send avatar as first message
                            if self.avatar_file and os.path.exists(self.avatar_file):
                                try:
                                    avatar_image = discord.File(self.avatar_file, filename="avatar.png")
                                    await interaction.response.send_message(embed=avatar_embed, file=avatar_image, ephemeral=True)
                                except Exception:
                                    # If file fails, just use URL
                                    await interaction.response.send_message(embed=avatar_embed, ephemeral=True)
                            else:
                                await interaction.response.send_message(embed=avatar_embed, ephemeral=True)
                        else:
                            # No avatar, need to respond to interaction first
                            pass
                        
                        # Now send description text
                        # Discord embed description limit is 4096 characters
                        if len(description_text) <= 4096:
                            desc_embed = discord.Embed(
                                title=f"Description",
                                description=description_text,
                                color=discord.Color.blue()
                            )
                            if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                                # Avatar was sent, use followup
                                await interaction.followup.send(embed=desc_embed, ephemeral=True)
                            else:
                                # No avatar, this is the first response
                                await interaction.response.send_message(embed=desc_embed, ephemeral=True)
                        else:
                            # Split long descriptions into multiple embeds
                            chunks = split_text_intelligently(description_text, max_chunk_size=4000)
                            
                            if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                                # Avatar was sent, all chunks are followups
                                for i, chunk in enumerate(chunks, start=1):
                                    follow_embed = discord.Embed(
                                        title=f"Description (Part {i}/{len(chunks)})",
                                        description=chunk,
                                        color=discord.Color.blue()
                                    )
                                    await interaction.followup.send(embed=follow_embed, ephemeral=True)
                            else:
                                # No avatar, send first chunk as response
                                first_embed = discord.Embed(
                                    title=f"Description (Part 1/{len(chunks)})",
                                    description=chunks[0],
                                    color=discord.Color.blue()
                                )
                                await interaction.response.send_message(embed=first_embed, ephemeral=True)
                                
                                # Send remaining chunks as follow-ups
                                for i, chunk in enumerate(chunks[1:], start=2):
                                    follow_embed = discord.Embed(
                                        title=f"Description (Part {i}/{len(chunks)})",
                                        description=chunk,
                                        color=discord.Color.blue()
                                    )
                                    await interaction.followup.send(embed=follow_embed, ephemeral=True)
                
                view = DescriptionView(user_char.get("description", ""), user_char.get("avatar_url", ""), user_char.get("avatar_file", ""))
                await ctx.send(embed=embed, view=view)
                
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        
        @self.command(name='set')
        async def set_user_character(ctx, user_character_name: str):
            """
            Manually set your active user character
            Usage: !set <character_name>
            Example: !set alice
            
            This allows you to set your active user character without using !chat.
            Your set character will be shown when you use !viewu.
            """
            try:
                # Check if the user character exists
                user_char = self.config_manager.get_user_character_by_name(user_character_name)
                if not user_char:
                    await ctx.send(f"Error: User character '{user_character_name}' not found. Use the GUI or create it first.")
                    return
                
                # Store this as the user's active character by adding it to chat history
                # This way it will be picked up by !viewu and !chat
                channel_id = str(ctx.channel.id)
                message_data = {
                    "author": str(ctx.author.id),
                    "author_name": str(ctx.author.name),
                    "user_character": user_character_name,
                    "content": f"[Set active character to {user_char.get('display_name', user_character_name)}]",
                    "type": "system",  # Mark as system message so it doesn't interfere with chat
                    "timestamp": ctx.message.created_at.isoformat()
                }
                self.config_manager.add_chat_message(channel_id, message_data)
                
                await ctx.send(f"✓ Your active user character is now '{user_char.get('display_name', user_character_name)}'. Use !viewu to confirm.")
                
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        
        @self.command(name='config')
        @commands.has_permissions(administrator=True)
        async def config_menu(ctx):
            """
            Open interactive configuration menu (Admin only)
            Usage: !config
            
            This command opens an interactive menu with buttons to:
            - Configure OpenAI settings
            - View and manage AI characters
            - View and manage user characters
            - View bot settings (reconnection config)
            - View lorebooks
            - View presets
            """
            try:
                embed = discord.Embed(
                    title="🎛️ Bot Configuration Menu",
                    description="Use the buttons below to configure the bot.\n\n"
                               "**Available Options:**\n"
                               "🔧 **OpenAI Config** - Configure API settings\n"
                               "🤖 **Characters** - View AI characters\n"
                               "👥 **User Characters** - View user/player characters\n"
                               "⚙️ **Bot Settings** - View reconnection settings\n"
                               "📚 **Lorebooks** - View available lorebooks\n"
                               "🎯 **Presets** - View AI presets\n",
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Configuration menu expires after 3 minutes of inactivity")
                
                view = ConfigMenuView(self.config_manager, self.ai_handler, timeout=180)
                await ctx.send(embed=embed, view=view)
                
            except Exception as e:
                await ctx.send(f"Error opening configuration menu: {str(e)}")
        
        @self.command(name='viewc')
        async def viewc(ctx, character_name: Optional[str] = None):
            """
            View the current AI/Bot character for this channel
            Usage: !viewc
            Or: !viewc <character_name> to view a specific character
            """
            try:
                # If a specific character name is provided, show that character
                if character_name:
                    char = self.config_manager.get_character_by_name(character_name)
                    if not char:
                        await ctx.send(f"Error: Character '{character_name}' not found.")
                        return
                else:
                    # Get the channel's active character
                    channel_id = str(ctx.channel.id)
                    ai_character_name = self.config_manager.get_channel_character(channel_id)
                    
                    if not ai_character_name:
                        # Use default character (first one)
                        characters = self.config_manager.get_characters()
                        if characters:
                            char = characters[0]
                            await ctx.send(f"No character set for this channel. Showing default character:")
                        else:
                            await ctx.send("No characters configured.")
                            return
                    else:
                        char = self.config_manager.get_character_by_name(ai_character_name)
                        if not char:
                            await ctx.send(f"Error: Channel character '{ai_character_name}' was not found in the config.")
                            return
                
                # Create an embed to display the character info
                embed = discord.Embed(
                    title=f"AI Character: {char.get('display_name', char.get('name', 'Unknown'))}",
                    color=discord.Color.blue()
                )
                
                embed.add_field(name="Character ID", value=char.get("name", "Unknown"), inline=False)
                
                # Add avatar if available
                avatar_url = char.get("avatar_url", "")
                if avatar_url:
                    embed.set_thumbnail(url=avatar_url)
                
                # Create a view with buttons to show description and scenario
                class CharacterView(discord.ui.View):
                    def __init__(self, description, scenario, avatar_url, avatar_file):
                        super().__init__(timeout=300)  # 5 minute timeout
                        self.description = description
                        self.scenario = scenario
                        self.avatar_url = avatar_url
                        self.avatar_file = avatar_file
                    
                    @discord.ui.button(label="Show Description", style=discord.ButtonStyle.primary)
                    async def show_description(self, interaction: discord.Interaction, button: discord.ui.Button):
                        description_text = self.description if self.description else "No description available."
                        
                        # Send avatar image first if available
                        if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                            avatar_embed = discord.Embed(
                                title="Avatar",
                                color=discord.Color.blue()
                            )
                            
                            # Set the image in the embed
                            if self.avatar_url:
                                avatar_embed.set_image(url=self.avatar_url)
                            
                            # Send avatar as first message
                            if self.avatar_file and os.path.exists(self.avatar_file):
                                try:
                                    avatar_image = discord.File(self.avatar_file, filename="avatar.png")
                                    await interaction.response.send_message(embed=avatar_embed, file=avatar_image, ephemeral=True)
                                except Exception:
                                    # If file fails, just use URL
                                    await interaction.response.send_message(embed=avatar_embed, ephemeral=True)
                            else:
                                await interaction.response.send_message(embed=avatar_embed, ephemeral=True)
                        else:
                            # No avatar, need to respond to interaction first
                            pass
                        
                        # Now send description text
                        # Discord embed description limit is 4096 characters
                        if len(description_text) <= 4096:
                            desc_embed = discord.Embed(
                                title=f"Description",
                                description=description_text,
                                color=discord.Color.blue()
                            )
                            if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                                # Avatar was sent, use followup
                                await interaction.followup.send(embed=desc_embed, ephemeral=True)
                            else:
                                # No avatar, this is the first response
                                await interaction.response.send_message(embed=desc_embed, ephemeral=True)
                        else:
                            # Split long descriptions into multiple embeds
                            chunks = split_text_intelligently(description_text, max_chunk_size=4000)
                            
                            if self.avatar_url or (self.avatar_file and os.path.exists(self.avatar_file)):
                                # Avatar was sent, all chunks are followups
                                for i, chunk in enumerate(chunks, start=1):
                                    follow_embed = discord.Embed(
                                        title=f"Description (Part {i}/{len(chunks)})",
                                        description=chunk,
                                        color=discord.Color.blue()
                                    )
                                    await interaction.followup.send(embed=follow_embed, ephemeral=True)
                            else:
                                # No avatar, send first chunk as response
                                first_embed = discord.Embed(
                                    title=f"Description (Part 1/{len(chunks)})",
                                    description=chunks[0],
                                    color=discord.Color.blue()
                                )
                                await interaction.response.send_message(embed=first_embed, ephemeral=True)
                                
                                # Send remaining chunks as follow-ups
                                for i, chunk in enumerate(chunks[1:], start=2):
                                    follow_embed = discord.Embed(
                                        title=f"Description (Part {i}/{len(chunks)})",
                                        description=chunk,
                                        color=discord.Color.blue()
                                    )
                                    await interaction.followup.send(embed=follow_embed, ephemeral=True)
                    
                    @discord.ui.button(label="Show Scenario", style=discord.ButtonStyle.secondary)
                    async def show_scenario(self, interaction: discord.Interaction, button: discord.ui.Button):
                        scenario_text = self.scenario if self.scenario else "No scenario available."
                        
                        # Discord embed description limit is 4096 characters
                        if len(scenario_text) <= 4096:
                            scenario_embed = discord.Embed(
                                title=f"Scenario",
                                description=scenario_text,
                                color=discord.Color.blue()
                            )
                            await interaction.response.send_message(embed=scenario_embed, ephemeral=True)
                        else:
                            # Split long scenarios into multiple embeds
                            chunks = split_text_intelligently(scenario_text, max_chunk_size=4000)
                            
                            # Send first chunk as response
                            first_embed = discord.Embed(
                                title=f"Scenario (Part 1/{len(chunks)})",
                                description=chunks[0],
                                color=discord.Color.blue()
                            )
                            await interaction.response.send_message(embed=first_embed, ephemeral=True)
                            
                            # Send remaining chunks as follow-ups
                            for i, chunk in enumerate(chunks[1:], start=2):
                                follow_embed = discord.Embed(
                                    title=f"Scenario (Part {i}/{len(chunks)})",
                                    description=chunk,
                                    color=discord.Color.blue()
                                )
                                await interaction.followup.send(embed=follow_embed, ephemeral=True)
                
                view = CharacterView(char.get("description", ""), char.get("scenario", ""), char.get("avatar_url", ""), char.get("avatar_file", ""))
                await ctx.send(embed=embed, view=view)
                
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        
        @self.command(name='lorebook')
        async def lorebook(ctx, action: str, *args):
            """
            Manage lorebooks
            Usage: 
              !lorebook create <name> - Create a new lorebook
              !lorebook list - List all lorebooks
              !lorebook activate <name> - Activate a lorebook
              !lorebook deactivate <name> - Deactivate a lorebook
              !lorebook delete <name> - Delete a lorebook
              !lorebook show <name> - Show entries in a lorebook
              !lorebook addentry <lorebook_name> <constant|normal> <content> [keywords...] 
                - Add entry (keywords only for normal type, use quotes for multi-word content)
              !lorebook delentry <lorebook_name> <entry_index> - Delete entry by index
            """
            # Reload config to get latest lorebook updates from GUI
            self.config_manager.reload_config()
            
            action = action.lower()
            
            if action == "create":
                if len(args) < 1:
                    await ctx.send("Usage: !lorebook create <name>")
                    return
                name = args[0]
                
                # Check if lorebook already exists
                if self.config_manager.get_lorebook_by_name(name):
                    await ctx.send(f"Error: Lorebook '{name}' already exists.")
                    return
                
                self.config_manager.add_lorebook(name, active=True)
                await ctx.send(f"✓ Lorebook '{name}' created and activated.")
            
            elif action == "list":
                lorebooks = self.config_manager.get_lorebooks()
                if not lorebooks:
                    await ctx.send("No lorebooks found. Use `!lorebook create <name>` to create one.")
                    return
                
                lines = ["**Lorebooks:**"]
                for i, lb in enumerate(lorebooks):
                    status = "✓ Active" if lb.get("active", False) else "✗ Inactive"
                    entry_count = len(lb.get("entries", []))
                    lines.append(f"{i+1}. **{lb.get('name')}** - {status} ({entry_count} entries)")
                
                await ctx.send("\n".join(lines))
            
            elif action == "activate":
                if len(args) < 1:
                    await ctx.send("Usage: !lorebook activate <name>")
                    return
                name = args[0]
                
                if self.config_manager.toggle_lorebook_active(name, True):
                    await ctx.send(f"✓ Lorebook '{name}' activated.")
                else:
                    await ctx.send(f"Error: Lorebook '{name}' not found.")
            
            elif action == "deactivate":
                if len(args) < 1:
                    await ctx.send("Usage: !lorebook deactivate <name>")
                    return
                name = args[0]
                
                if self.config_manager.toggle_lorebook_active(name, False):
                    await ctx.send(f"✓ Lorebook '{name}' deactivated.")
                else:
                    await ctx.send(f"Error: Lorebook '{name}' not found.")
            
            elif action == "delete":
                if len(args) < 1:
                    await ctx.send("Usage: !lorebook delete <name>")
                    return
                name = args[0]
                
                index = self.config_manager.get_lorebook_index_by_name(name)
                if index is not None:
                    self.config_manager.delete_lorebook(index)
                    await ctx.send(f"✓ Lorebook '{name}' deleted.")
                else:
                    await ctx.send(f"Error: Lorebook '{name}' not found.")
            
            elif action == "show":
                if len(args) < 1:
                    await ctx.send("Usage: !lorebook show <name>")
                    return
                name = args[0]
                
                lorebook = self.config_manager.get_lorebook_by_name(name)
                if not lorebook:
                    await ctx.send(f"Error: Lorebook '{name}' not found.")
                    return
                
                entries = lorebook.get("entries", [])
                if not entries:
                    await ctx.send(f"Lorebook '{name}' has no entries.")
                    return
                
                status = "Active" if lorebook.get("active", False) else "Inactive"
                lines = [f"**Lorebook: {name}** ({status})"]
                lines.append("")
                
                for i, entry in enumerate(entries):
                    entry_type = entry.get("insertion_type", "normal").upper()
                    content = entry.get("content", "")
                    keywords = entry.get("keywords", [])
                    
                    # Truncate long content for display
                    if len(content) > 100:
                        content = content[:100] + "..."
                    
                    lines.append(f"**Entry {i}** [{entry_type}]")
                    lines.append(f"  Content: {content}")
                    if entry_type == "NORMAL" and keywords:
                        lines.append(f"  Keywords: {', '.join(keywords)}")
                    lines.append("")
                
                # Discord has a 2000 character limit, so we might need to split
                message = "\n".join(lines)
                if len(message) <= 2000:
                    await ctx.send(message)
                else:
                    # Send in chunks
                    chunks = [message[i:i+1900] for i in range(0, len(message), 1900)]
                    for chunk in chunks:
                        await ctx.send(chunk)
            
            elif action == "addentry":
                if len(args) < 3:
                    await ctx.send("Usage: !lorebook addentry <lorebook_name> <constant|normal> <content> [keywords...]")
                    return
                
                lorebook_name = args[0]
                insertion_type = args[1].lower()
                
                if insertion_type not in ["constant", "normal"]:
                    await ctx.send("Error: Insertion type must be 'constant' or 'normal'.")
                    return
                
                # Content is the third argument
                content = args[2]
                
                # Keywords are remaining arguments (only for normal type)
                keywords = []
                if insertion_type == "normal" and len(args) > 3:
                    keywords = list(args[3:])
                
                if self.config_manager.add_lorebook_entry(lorebook_name, content, insertion_type, keywords):
                    if insertion_type == "constant":
                        await ctx.send(f"✓ Constant entry added to lorebook '{lorebook_name}'.")
                    else:
                        kw_str = f" with keywords: {', '.join(keywords)}" if keywords else " (no keywords)"
                        await ctx.send(f"✓ Normal entry added to lorebook '{lorebook_name}'{kw_str}.")
                else:
                    await ctx.send(f"Error: Lorebook '{lorebook_name}' not found or invalid insertion type.")
            
            elif action == "delentry":
                if len(args) < 2:
                    await ctx.send("Usage: !lorebook delentry <lorebook_name> <entry_index>")
                    return
                
                lorebook_name = args[0]
                try:
                    entry_index = int(args[1])
                except ValueError:
                    await ctx.send("Error: Entry index must be a number.")
                    return
                
                if self.config_manager.delete_lorebook_entry(lorebook_name, entry_index):
                    await ctx.send(f"✓ Entry {entry_index} deleted from lorebook '{lorebook_name}'.")
                else:
                    await ctx.send(f"Error: Could not delete entry. Check lorebook name and entry index.")
            
            else:
                await ctx.send(f"Unknown action '{action}'. Use: create, list, activate, deactivate, delete, show, addentry, delentry")
    
    async def send_via_webhook(self, channel, content: str, character: Dict[str, Any]) -> None:
        """
        Send a message via webhook with character identity
        Handles long messages by splitting into chunks, with avatar sent first
        
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
        
        # Prepare avatar - use URL if available, otherwise attach local file
        avatar_image = None
        if avatar_file and os.path.exists(avatar_file):
            # Attach local avatar file as an image in the message
            try:
                avatar_image = discord.File(avatar_file, filename="avatar.png")
            except Exception:
                pass
        
        # Discord message limit is 2000 characters
        # If content is short enough, send in one message
        if len(content) <= 2000:
            if avatar_url:
                # Use avatar_url for webhook avatar (preferred method)
                if avatar_image:
                    # Both URL and local file - use URL for avatar, attach file
                    await webhook.send(content=content, username=display_name, avatar_url=avatar_url, file=avatar_image)
                else:
                    await webhook.send(content=content, username=display_name, avatar_url=avatar_url)
            elif avatar_image:
                # Only local file - attach it to the message
                await webhook.send(content=content, username=display_name, file=avatar_image)
            else:
                # No avatar
                await webhook.send(content=content, username=display_name)
        else:
            # Content is too long - need to split intelligently at sentence boundaries
            chunks = split_text_intelligently(content, max_chunk_size=1900)
            
            # If we have an avatar image file, send it FIRST as a separate message
            # This ensures the image appears before the text chunks
            if avatar_image:
                # Send avatar image first on its own
                if avatar_url:
                    # Use URL for avatar icon
                    await webhook.send(content="", username=display_name, avatar_url=avatar_url, file=avatar_image)
                else:
                    # Just the file
                    await webhook.send(content="", username=display_name, file=avatar_image)
                
                # Now send all text chunks (no need to attach image again)
                for chunk in chunks:
                    if avatar_url:
                        await webhook.send(content=chunk, username=display_name, avatar_url=avatar_url)
                    else:
                        await webhook.send(content=chunk, username=display_name)
            else:
                # No avatar file, send chunks with avatar_url if available
                for chunk in chunks:
                    if avatar_url:
                        await webhook.send(content=chunk, username=display_name, avatar_url=avatar_url)
                    else:
                        await webhook.send(content=chunk, username=display_name)
    
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
        
        @self.event
        async def on_command_error(ctx, error):
            """Handle command errors gracefully"""
            # Handle missing required argument (e.g., when message parsing fails with newlines)
            if isinstance(error, commands.MissingRequiredArgument):
                if error.param.name == 'message':
                    await ctx.send("Please provide a message after the command. Usage: `!chat [character]: your message here`")
                else:
                    await ctx.send(f"Missing required argument: {error.param.name}")
                return
            
            # Handle bad argument errors
            if isinstance(error, commands.BadArgument):
                await ctx.send(f"Invalid argument provided: {str(error)}")
                return
            
            # Handle command not found (ignore silently - might be a message to another bot)
            if isinstance(error, commands.CommandNotFound):
                return
            
            # Handle other errors
            print(f"Command error in {ctx.command}: {str(error)}")
            import traceback
            print(traceback.format_exc())
            
            # Don't expose internal errors to users
            await ctx.send("An error occurred while processing the command. Please check the console for details.")


def _handle_retry(reconnect_enabled: bool, retry_count: int, max_retries: int, 
                 base_delay: int, max_delay: int) -> bool:
    """
    Handle retry logic for connection failures.
    
    Returns:
        bool: True if should retry, False if should exit
    """
    if not reconnect_enabled:
        print("Reconnection is disabled. Exiting.")
        return False
    
    if retry_count >= max_retries:
        print(f"Max retries ({max_retries}) reached. Giving up.")
        return False
    
    # Calculate delay with exponential backoff
    delay = min(base_delay * (2 ** (retry_count - 1)), max_delay)
    print(f"Will retry in {delay} seconds... (Attempt {retry_count}/{max_retries})")
    time.sleep(delay)
    return True


def main():
    """Main entry point with automatic reconnection"""
    config_manager = ConfigManager()
    
    token = config_manager.get_discord_token()
    if not token:
        print("Error: Discord bot token not configured.")
        print("Please edit config.json and add your Discord bot token.")
        return
    
    reconnect_config = config_manager.get_reconnect_config()
    reconnect_enabled = reconnect_config.get("enabled", True)
    max_retries = reconnect_config.get("max_retries", 10)
    base_delay = reconnect_config.get("base_delay", 5)
    max_delay = reconnect_config.get("max_delay", 300)
    
    retry_count = 0
    
    while True:
        try:
            # Create a new bot instance for each connection attempt
            bot = PresetBot(config_manager)
            
            print(f"Starting Discord bot... (Attempt {retry_count + 1})")
            if retry_count > 0:
                print(f"  Reconnection enabled: {reconnect_enabled}")
                print(f"  Max retries: {max_retries}")
            
            # Run the bot
            bot.run(token, reconnect=True)
            
            # If we get here, the bot was shut down intentionally
            print("Bot shut down gracefully.")
            break
            
        except discord.LoginFailure as e:
            print(f"\n[ERROR] Login failed: {str(e)}")
            print("Please check your Discord bot token in config.json")
            print("The token may be invalid or expired.")
            break  # Don't retry on login failures - token needs to be fixed
            
        except discord.HTTPException as e:
            print(f"\n[ERROR] HTTP Exception: {str(e)}")
            retry_count += 1
            if not _handle_retry(reconnect_enabled, retry_count, max_retries, base_delay, max_delay):
                break
            
        except discord.GatewayNotFound as e:
            print(f"\n[ERROR] Gateway not found: {str(e)}")
            print("Discord's gateway service may be down.")
            retry_count += 1
            if not _handle_retry(reconnect_enabled, retry_count, max_retries, base_delay, max_delay):
                break
            
        except KeyboardInterrupt:
            print("\n[INFO] Received keyboard interrupt. Shutting down...")
            break
            
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            retry_count += 1
            if not _handle_retry(reconnect_enabled, retry_count, max_retries, base_delay, max_delay):
                break


if __name__ == "__main__":
    main()
