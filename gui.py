"""
Preset Bot - GUI Configuration and Manual Send Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import asyncio
import threading
import shutil
from typing import Optional
from bot import ConfigManager, AIResponseHandler
import discord


class PresetBotGUI:
    """GUI for configuring the bot and sending manual messages"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Preset Discord Bot - Configuration & Manual Send")
        self.root.geometry("800x700")
        
        self.config_manager = ConfigManager()
        self.ai_handler = AIResponseHandler(self.config_manager)
        self.discord_client = None
        
        self.create_widgets()
        self.load_current_config()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration Tab
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuration")
        self.create_config_tab()
        
        # Presets Tab
        self.presets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.presets_frame, text="Presets")
        self.create_presets_tab()
        
        # Manual Send Tab
        self.manual_send_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manual_send_frame, text="Manual Send")
        self.create_manual_send_tab()
        
        # Characters Tab
        self.characters_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.characters_frame, text="Characters")
        self.create_characters_tab()
        
        # User Characters Tab
        self.user_characters_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.user_characters_frame, text="User Characters")
        self.create_user_characters_tab()
    
    def create_config_tab(self):
        """Create configuration tab"""
        
        # Discord Configuration
        discord_frame = ttk.LabelFrame(self.config_frame, text="Discord Configuration", padding=10)
        discord_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(discord_frame, text="Bot Token:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.discord_token_entry = ttk.Entry(discord_frame, width=50, show="*")
        self.discord_token_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # OpenAI Configuration
        openai_frame = ttk.LabelFrame(self.config_frame, text="OpenAI Compatible API Configuration", padding=10)
        openai_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(openai_frame, text="Base URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.openai_base_url_entry = ttk.Entry(openai_frame, width=50)
        self.openai_base_url_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(openai_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.openai_api_key_entry = ttk.Entry(openai_frame, width=50, show="*")
        self.openai_api_key_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Model Selection
        ttk.Label(openai_frame, text="Model:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(openai_frame, textvariable=self.model_var, width=47)
        self.model_dropdown.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Fetch Models button
        ttk.Button(openai_frame, text="Fetch Models", command=self.fetch_models).grid(row=2, column=2, pady=5, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(self.config_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Configuration", command=self.load_current_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test OpenAI Connection", command=self.test_openai).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.config_status_label = ttk.Label(self.config_frame, text="", foreground="blue")
        self.config_status_label.pack(pady=5)
    
    def create_manual_send_tab(self):
        """Create manual send tab"""
        
        # Server and Channel Configuration
        target_frame = ttk.LabelFrame(self.manual_send_frame, text="Target Configuration", padding=10)
        target_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(target_frame, text="Server ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_id_entry = ttk.Entry(target_frame, width=30)
        self.server_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(target_frame, text="Channel ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.channel_id_entry = ttk.Entry(target_frame, width=30)
        self.channel_id_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Character Selection
        character_frame = ttk.LabelFrame(self.manual_send_frame, text="Character Selection", padding=10)
        character_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(character_frame, text="Character:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.character_var = tk.StringVar()
        self.character_dropdown = ttk.Combobox(character_frame, textvariable=self.character_var, width=30, state="readonly")
        self.character_dropdown.grid(row=0, column=1, pady=5, padx=5)
        self.update_character_dropdown()
        
        # Message Input
        message_frame = ttk.LabelFrame(self.manual_send_frame, text="Message", padding=10)
        message_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.message_text = scrolledtext.ScrolledText(message_frame, height=10, width=70)
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.manual_send_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Send Message", command=self.send_manual_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_message).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.send_status_label = ttk.Label(self.manual_send_frame, text="", foreground="blue")
        self.send_status_label.pack(pady=5)
    
    def create_characters_tab(self):
        """Create characters management tab"""
        
        # Add Character
        add_frame = ttk.LabelFrame(self.characters_frame, text="Add New Character", padding=10)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Character Name (ID)
        ttk.Label(add_frame, text="Character Name (ID):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.char_name_entry = ttk.Entry(add_frame, width=30)
        self.char_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(lowercase, no spaces)", font=('TkDefaultFont', 8, 'italic')).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Display Name
        ttk.Label(add_frame, text="Display Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.char_display_name_entry = ttk.Entry(add_frame, width=30)
        self.char_display_name_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(shown in Discord)", font=('TkDefaultFont', 8, 'italic')).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Description
        ttk.Label(add_frame, text="Description:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.char_description_text = scrolledtext.ScrolledText(add_frame, height=5, width=50)
        self.char_description_text.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(AI system prompt)", font=('TkDefaultFont', 8, 'italic')).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Avatar selection
        avatar_frame = ttk.LabelFrame(add_frame, text="Avatar/Icon", padding=5)
        avatar_frame.grid(row=4, column=0, columnspan=3, sticky=tk.EW, pady=10, padx=5)
        
        # Avatar URL option
        ttk.Label(avatar_frame, text="Avatar URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.char_avatar_url_entry = ttk.Entry(avatar_frame, width=40)
        self.char_avatar_url_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        # OR separator
        ttk.Label(avatar_frame, text="--- OR ---").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Avatar file option
        ttk.Label(avatar_frame, text="Avatar File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.char_avatar_file_var = tk.StringVar()
        self.char_avatar_file_entry = ttk.Entry(avatar_frame, width=30, textvariable=self.char_avatar_file_var, state='readonly')
        self.char_avatar_file_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(avatar_frame, text="Browse...", command=self.browse_avatar_file).grid(row=2, column=2, pady=5, padx=5)
        
        ttk.Button(add_frame, text="Add Character", command=self.add_character).grid(row=5, column=1, pady=10)
        
        # List Characters
        list_frame = ttk.LabelFrame(self.characters_frame, text="Current Characters", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.characters_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
        self.characters_listbox.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.LEFT)
        scrollbar.config(command=self.characters_listbox.yview)
        
        # Buttons for character management
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Refresh List", command=self.refresh_characters_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_character).pack(side=tk.LEFT, padx=5)
        
        self.refresh_characters_list()
    
    def browse_avatar_file(self):
        """Browse for avatar image file"""
        filename = filedialog.askopenfilename(
            title="Select Avatar Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.char_avatar_file_var.set(filename)
    
    def load_current_config(self):
        """Load current configuration into GUI"""
        # Discord Token
        token = self.config_manager.get_discord_token()
        self.discord_token_entry.delete(0, tk.END)
        self.discord_token_entry.insert(0, token)
        
        # OpenAI Config
        openai_config = self.config_manager.get_openai_config()
        self.openai_base_url_entry.delete(0, tk.END)
        self.openai_base_url_entry.insert(0, openai_config.get("base_url", "https://api.openai.com/v1"))
        
        self.openai_api_key_entry.delete(0, tk.END)
        self.openai_api_key_entry.insert(0, openai_config.get("api_key", ""))
        
        # Model Selection
        available_models = self.config_manager.get_available_models()
        if available_models:
            self.model_dropdown['values'] = available_models
        selected_model = self.config_manager.get_selected_model()
        self.model_var.set(selected_model)
        
        # Last Manual Send Target
        last_target = self.config_manager.get_last_manual_send_target()
        self.server_id_entry.delete(0, tk.END)
        self.server_id_entry.insert(0, last_target.get("server_id", ""))
        self.channel_id_entry.delete(0, tk.END)
        self.channel_id_entry.insert(0, last_target.get("channel_id", ""))
        
        self.config_status_label.config(text="Configuration loaded", foreground="green")
    
    def save_config(self):
        """Save configuration from GUI"""
        try:
            # Save Discord Token
            token = self.discord_token_entry.get()
            if token:
                self.config_manager.set_discord_token(token)
            
            # Save OpenAI Config
            base_url = self.openai_base_url_entry.get()
            api_key = self.openai_api_key_entry.get()
            if base_url and api_key:
                self.config_manager.set_openai_config(base_url, api_key)
                self.ai_handler.update_client()
            
            # Save selected model
            model = self.model_var.get()
            if model:
                self.config_manager.set_selected_model(model)
            
            self.config_status_label.config(text="Configuration saved successfully!", foreground="green")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            self.config_status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def test_openai(self):
        """Test OpenAI connection"""
        self.config_status_label.config(text="Testing OpenAI connection...", foreground="blue")
        
        def test():
            try:
                # Save current config first
                base_url = self.openai_base_url_entry.get()
                api_key = self.openai_api_key_entry.get()
                if base_url and api_key:
                    self.config_manager.set_openai_config(base_url, api_key)
                    self.ai_handler.update_client()
                
                # Test with a simple message
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    self.ai_handler.get_ai_response("Say 'Connection successful!'")
                )
                loop.close()
                
                if "Error" not in response:
                    self.config_status_label.config(text="OpenAI connection successful!", foreground="green")
                    messagebox.showinfo("Success", f"Connection successful!\nResponse: {response[:100]}...")
                else:
                    self.config_status_label.config(text="Connection failed", foreground="red")
                    messagebox.showerror("Error", response)
            except Exception as e:
                self.config_status_label.config(text=f"Error: {str(e)}", foreground="red")
                messagebox.showerror("Error", f"Connection failed: {str(e)}")
        
        threading.Thread(target=test, daemon=True).start()
    
    def fetch_models(self):
        """Fetch available models from API"""
        self.config_status_label.config(text="Fetching models...", foreground="blue")
        
        def fetch():
            try:
                # Save current config first
                base_url = self.openai_base_url_entry.get()
                api_key = self.openai_api_key_entry.get()
                if base_url and api_key:
                    self.config_manager.set_openai_config(base_url, api_key)
                    self.ai_handler.update_client()
                
                # Fetch models
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                models = loop.run_until_complete(
                    self.ai_handler.fetch_available_models()
                )
                loop.close()
                
                if models:
                    self.model_dropdown['values'] = models
                    if models:
                        self.model_var.set(models[0])
                    self.config_status_label.config(text=f"Fetched {len(models)} models successfully!", foreground="green")
                    messagebox.showinfo("Success", f"Fetched {len(models)} models from API")
                else:
                    self.config_status_label.config(text="No models found or error fetching", foreground="red")
                    messagebox.showwarning("Warning", "No models found. Check your API configuration.")
            except Exception as e:
                self.config_status_label.config(text=f"Error: {str(e)}", foreground="red")
                messagebox.showerror("Error", f"Failed to fetch models: {str(e)}")
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def send_manual_message(self):
        """Send manual message through Discord bot using webhook - sends message directly without AI processing"""
        server_id = self.server_id_entry.get()
        channel_id = self.channel_id_entry.get()
        character = self.character_var.get()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not server_id or not channel_id:
            messagebox.showerror("Error", "Please enter both Server ID and Channel ID")
            return
        
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        if not character:
            messagebox.showerror("Error", "Please select a character")
            return
        
        # Save last used server and channel IDs
        self.config_manager.set_last_manual_send_target(server_id, channel_id)
        
        self.send_status_label.config(text="Sending message...", foreground="blue")
        
        def send():
            try:
                # Get character data
                char_data = self.config_manager.get_character_by_name(character)
                if not char_data:
                    self.send_status_label.config(text="Character not found", foreground="red")
                    messagebox.showerror("Error", f"Character '{character}' not found")
                    return
                
                # Skip AI processing - send message directly
                # The message is sent as-is from the selected character
                
                # Initialize Discord client if needed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if not self.discord_client:
                    self.discord_client = discord.Client(intents=discord.Intents.default())
                    
                    @self.discord_client.event
                    async def on_ready():
                        try:
                            channel = self.discord_client.get_channel(int(channel_id))
                            if channel:
                                # Send via webhook - use the message directly without AI processing
                                await self.send_via_webhook(channel, message, char_data)
                                self.send_status_label.config(text=f"Message sent successfully!", foreground="green")
                                messagebox.showinfo("Success", f"Message sent to channel {channel_id} as {char_data.get('display_name', character)}")
                            else:
                                self.send_status_label.config(text="Channel not found", foreground="red")
                                messagebox.showerror("Error", f"Channel {channel_id} not found")
                        except Exception as e:
                            self.send_status_label.config(text=f"Error: {str(e)}", foreground="red")
                            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
                        finally:
                            await self.discord_client.close()
                    
                    token = self.config_manager.get_discord_token()
                    if not token:
                        self.send_status_label.config(text="Discord token not configured", foreground="red")
                        messagebox.showerror("Error", "Please configure Discord bot token first")
                        return
                    
                    loop.run_until_complete(self.discord_client.start(token))
                    self.discord_client = None
                
                loop.close()
            except Exception as e:
                self.send_status_label.config(text=f"Error: {str(e)}", foreground="red")
                messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        
        threading.Thread(target=send, daemon=True).start()
    
    async def send_via_webhook(self, channel, content: str, character: dict) -> None:
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
        
        # Send via webhook
        if avatar_url:
            await webhook.send(content=content, username=display_name, avatar_url=avatar_url)
        else:
            await webhook.send(content=content, username=display_name)
    
    def clear_message(self):
        """Clear message text"""
        self.message_text.delete("1.0", tk.END)
    
    def update_character_dropdown(self):
        """Update character dropdown with current characters"""
        characters = self.config_manager.get_characters()
        character_names = [char.get("name", "unknown") for char in characters]
        self.character_dropdown['values'] = character_names
        if character_names:
            self.character_var.set(character_names[0])
    
    def add_character(self):
        """Add a new character"""
        name = self.char_name_entry.get().strip().lower().replace(" ", "_")
        display_name = self.char_display_name_entry.get().strip()
        description = self.char_description_text.get("1.0", tk.END).strip()
        avatar_url = self.char_avatar_url_entry.get().strip()
        avatar_file_source = self.char_avatar_file_var.get().strip()
        
        if not name or not display_name or not description:
            messagebox.showerror("Error", "Please enter character name, display name, and description")
            return
        
        try:
            # Handle avatar file if provided
            avatar_file_dest = ""
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Create avatars directory if it doesn't exist
                avatars_dir = "character_avatars"
                os.makedirs(avatars_dir, exist_ok=True)
                
                # Copy file to avatars directory with character name
                file_ext = os.path.splitext(avatar_file_source)[1]
                avatar_file_dest = os.path.join(avatars_dir, f"{name}{file_ext}")
                shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Add character to config
            self.config_manager.add_character(name, display_name, description, avatar_url, avatar_file_dest)
            
            # Clear form
            self.char_name_entry.delete(0, tk.END)
            self.char_display_name_entry.delete(0, tk.END)
            self.char_description_text.delete("1.0", tk.END)
            self.char_avatar_url_entry.delete(0, tk.END)
            self.char_avatar_file_var.set("")
            
            self.refresh_characters_list()
            self.update_character_dropdown()
            messagebox.showinfo("Success", f"Character '{display_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add character: {str(e)}")
    
    def delete_character(self):
        """Delete selected character"""
        selection = self.characters_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a character to delete")
            return
        
        index = selection[0]
        characters = self.config_manager.get_characters()
        if 0 <= index < len(characters):
            char_name = characters[index].get("display_name", characters[index].get("name", "Unknown"))
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete character '{char_name}'?"):
                try:
                    # Delete avatar file if it exists
                    avatar_file = characters[index].get("avatar_file", "")
                    if avatar_file and os.path.exists(avatar_file):
                        os.remove(avatar_file)
                    
                    self.config_manager.delete_character(index)
                    self.refresh_characters_list()
                    self.update_character_dropdown()
                    messagebox.showinfo("Success", f"Character '{char_name}' deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete character: {str(e)}")
    
    def refresh_characters_list(self):
        """Refresh the characters list"""
        self.characters_listbox.delete(0, tk.END)
        characters = self.config_manager.get_characters()
        for char in characters:
            display_name = char.get("display_name", char.get("name", "Unknown"))
            name_id = char.get("name", "unknown")
            description = char.get("description") or char.get("system_prompt", "No description")
            desc_preview = description[:40] + "..." if len(description) > 40 else description
            self.characters_listbox.insert(tk.END, f"{display_name} ({name_id}): {desc_preview}")
        self.update_character_dropdown()
    
    def create_presets_tab(self):
        """Create presets management tab"""
        
        # Create scrollable frame
        canvas = tk.Canvas(self.presets_frame)
        scrollbar = ttk.Scrollbar(self.presets_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # AI Configuration Section
        ai_config_frame = ttk.LabelFrame(scrollable_frame, text="AI Configuration Options", padding=10)
        ai_config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Context Length
        ttk.Label(ai_config_frame, text="Max Tokens / Context Length:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.preset_max_tokens = ttk.Entry(ai_config_frame, width=15)
        self.preset_max_tokens.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        self.preset_max_tokens.insert(0, "4096")
        ttk.Label(ai_config_frame, text="(Max: 2000000)", font=('TkDefaultFont', 8, 'italic')).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Response Length
        ttk.Label(ai_config_frame, text="Response Length (Max Tokens):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.preset_response_length = ttk.Entry(ai_config_frame, width=15)
        self.preset_response_length.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        self.preset_response_length.insert(0, "1024")
        
        # Temperature
        ttk.Label(ai_config_frame, text="Temperature:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.preset_temperature = ttk.Entry(ai_config_frame, width=15)
        self.preset_temperature.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.preset_temperature.insert(0, "1.0")
        ttk.Label(ai_config_frame, text="(0.0 - 2.0)", font=('TkDefaultFont', 8, 'italic')).grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # Top P
        ttk.Label(ai_config_frame, text="Top P:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.preset_top_p = ttk.Entry(ai_config_frame, width=15)
        self.preset_top_p.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
        self.preset_top_p.insert(0, "1.0")
        ttk.Label(ai_config_frame, text="(0.0 - 1.0)", font=('TkDefaultFont', 8, 'italic')).grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # Model Reasoning
        ttk.Label(ai_config_frame, text="Model Reasoning:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.preset_reasoning_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(ai_config_frame, text="Enable", variable=self.preset_reasoning_var).grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Reasoning Level
        ttk.Label(ai_config_frame, text="Reasoning Level:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.preset_reasoning_level = ttk.Combobox(ai_config_frame, width=12, state="readonly")
        self.preset_reasoning_level['values'] = ['Auto', 'Maximum', 'High', 'Medium', 'Low', 'Minimum']
        self.preset_reasoning_level.current(0)
        self.preset_reasoning_level.grid(row=5, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Presence Penalty
        penalty_frame = ttk.Frame(ai_config_frame)
        penalty_frame.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        self.preset_use_presence_penalty = tk.BooleanVar(value=False)
        ttk.Checkbutton(penalty_frame, text="Use Presence Penalty:", variable=self.preset_use_presence_penalty).pack(side=tk.LEFT, padx=5)
        self.preset_presence_penalty = ttk.Entry(penalty_frame, width=15)
        self.preset_presence_penalty.pack(side=tk.LEFT, padx=5)
        self.preset_presence_penalty.insert(0, "0.0")
        ttk.Label(penalty_frame, text="(-2.0 - 2.0)", font=('TkDefaultFont', 8, 'italic')).pack(side=tk.LEFT, padx=5)
        
        # Frequency Penalty
        freq_frame = ttk.Frame(ai_config_frame)
        freq_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        self.preset_use_frequency_penalty = tk.BooleanVar(value=False)
        ttk.Checkbutton(freq_frame, text="Use Frequency Penalty:", variable=self.preset_use_frequency_penalty).pack(side=tk.LEFT, padx=5)
        self.preset_frequency_penalty = ttk.Entry(freq_frame, width=15)
        self.preset_frequency_penalty.pack(side=tk.LEFT, padx=5)
        self.preset_frequency_penalty.insert(0, "0.0")
        ttk.Label(freq_frame, text="(-2.0 - 2.0)", font=('TkDefaultFont', 8, 'italic')).pack(side=tk.LEFT, padx=5)
        
        # Preset Blocks Section
        blocks_frame = ttk.LabelFrame(scrollable_frame, text="Preset Message Blocks", padding=10)
        blocks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Block management
        self.preset_blocks = []
        
        ttk.Label(blocks_frame, text="Add message blocks that will be sent to the AI:").pack(anchor=tk.W, pady=5)
        
        # Add block button
        ttk.Button(blocks_frame, text="+ Add New Block", command=self.add_preset_block).pack(anchor=tk.W, pady=5)
        
        # Container for blocks
        self.blocks_container = ttk.Frame(blocks_frame)
        self.blocks_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Preset Management Section
        preset_mgmt_frame = ttk.LabelFrame(scrollable_frame, text="Preset Management", padding=10)
        preset_mgmt_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Preset name
        ttk.Label(preset_mgmt_frame, text="Preset Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.preset_name_entry = ttk.Entry(preset_mgmt_frame, width=30)
        self.preset_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(preset_mgmt_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save Preset", command=self.save_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Preset", command=self.load_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Set as Active", command=self.set_active_preset).pack(side=tk.LEFT, padx=5)
        
        # Preset list
        ttk.Label(preset_mgmt_frame, text="Saved Presets:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.preset_list_var = tk.StringVar()
        self.preset_list_dropdown = ttk.Combobox(preset_mgmt_frame, textvariable=self.preset_list_var, width=30, state="readonly")
        self.preset_list_dropdown.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.refresh_preset_list()
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_preset_block(self):
        """Add a new preset block to the UI"""
        block_frame = ttk.LabelFrame(self.blocks_container, text=f"Block {len(self.preset_blocks) + 1}", padding=5)
        block_frame.pack(fill=tk.X, pady=5)
        
        # Active checkbox
        active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(block_frame, text="Active", variable=active_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Role selection
        ttk.Label(block_frame, text="Role:").grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        role_var = tk.StringVar(value="system")
        role_combo = ttk.Combobox(block_frame, textvariable=role_var, width=12, state="readonly")
        role_combo['values'] = ['system', 'user', 'assistant']
        role_combo.grid(row=0, column=2, pady=2, padx=5, sticky=tk.W)
        
        # Content
        ttk.Label(block_frame, text="Content:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        content_text = scrolledtext.ScrolledText(block_frame, height=4, width=60)
        content_text.grid(row=1, column=1, columnspan=2, pady=2, padx=5, sticky=tk.W)
        
        # Delete button
        def delete_block():
            block_frame.destroy()
            self.preset_blocks.remove(block_data)
        
        ttk.Button(block_frame, text="Delete Block", command=delete_block).grid(row=2, column=1, pady=5)
        
        # Store block data
        block_data = {
            'frame': block_frame,
            'active_var': active_var,
            'role_var': role_var,
            'content_text': content_text
        }
        self.preset_blocks.append(block_data)
    
    def save_preset(self):
        """Save current preset configuration"""
        preset_name = self.preset_name_entry.get().strip()
        if not preset_name:
            messagebox.showerror("Error", "Please enter a preset name")
            return
        
        try:
            # Collect AI configuration
            ai_config = {
                "max_tokens": int(self.preset_max_tokens.get() or "4096"),
                "response_length": int(self.preset_response_length.get() or "1024"),
                "temperature": float(self.preset_temperature.get() or "1.0"),
                "top_p": float(self.preset_top_p.get() or "1.0"),
                "reasoning_enabled": self.preset_reasoning_var.get(),
                "reasoning_level": self.preset_reasoning_level.get(),
                "use_presence_penalty": self.preset_use_presence_penalty.get(),
                "presence_penalty": float(self.preset_presence_penalty.get() or "0.0"),
                "use_frequency_penalty": self.preset_use_frequency_penalty.get(),
                "frequency_penalty": float(self.preset_frequency_penalty.get() or "0.0")
            }
            
            # Validate max tokens
            if ai_config["max_tokens"] > 2000000:
                messagebox.showerror("Error", "Max tokens cannot exceed 2,000,000")
                return
            
            # Collect blocks
            blocks = []
            for block_data in self.preset_blocks:
                blocks.append({
                    "active": block_data['active_var'].get(),
                    "role": block_data['role_var'].get(),
                    "content": block_data['content_text'].get("1.0", tk.END).strip()
                })
            
            # Create preset
            preset = {
                "name": preset_name,
                "ai_config": ai_config,
                "blocks": blocks
            }
            
            # Check if preset exists
            existing = self.config_manager.get_preset_by_name(preset_name)
            if existing:
                if messagebox.askyesno("Confirm", f"Preset '{preset_name}' already exists. Overwrite?"):
                    presets = self.config_manager.get_presets()
                    for i, p in enumerate(presets):
                        if p.get("name") == preset_name:
                            self.config_manager.update_preset(i, preset)
                            break
                else:
                    return
            else:
                self.config_manager.add_preset(preset)
            
            self.refresh_preset_list()
            messagebox.showinfo("Success", f"Preset '{preset_name}' saved successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preset: {str(e)}")
    
    def load_preset(self):
        """Load selected preset into UI"""
        preset_name = self.preset_list_var.get()
        if not preset_name:
            messagebox.showwarning("Warning", "Please select a preset to load")
            return
        
        preset = self.config_manager.get_preset_by_name(preset_name)
        if not preset:
            messagebox.showerror("Error", "Preset not found")
            return
        
        # Load AI configuration
        ai_config = preset.get("ai_config", {})
        self.preset_max_tokens.delete(0, tk.END)
        self.preset_max_tokens.insert(0, str(ai_config.get("max_tokens", 4096)))
        
        self.preset_response_length.delete(0, tk.END)
        self.preset_response_length.insert(0, str(ai_config.get("response_length", 1024)))
        
        self.preset_temperature.delete(0, tk.END)
        self.preset_temperature.insert(0, str(ai_config.get("temperature", 1.0)))
        
        self.preset_top_p.delete(0, tk.END)
        self.preset_top_p.insert(0, str(ai_config.get("top_p", 1.0)))
        
        self.preset_reasoning_var.set(ai_config.get("reasoning_enabled", False))
        
        reasoning_level = ai_config.get("reasoning_level", "Auto")
        if reasoning_level in self.preset_reasoning_level['values']:
            self.preset_reasoning_level.set(reasoning_level)
        
        self.preset_use_presence_penalty.set(ai_config.get("use_presence_penalty", False))
        self.preset_presence_penalty.delete(0, tk.END)
        self.preset_presence_penalty.insert(0, str(ai_config.get("presence_penalty", 0.0)))
        
        self.preset_use_frequency_penalty.set(ai_config.get("use_frequency_penalty", False))
        self.preset_frequency_penalty.delete(0, tk.END)
        self.preset_frequency_penalty.insert(0, str(ai_config.get("frequency_penalty", 0.0)))
        
        # Clear existing blocks
        for block_data in self.preset_blocks[:]:
            block_data['frame'].destroy()
            self.preset_blocks.remove(block_data)
        
        # Load blocks
        for block in preset.get("blocks", []):
            self.add_preset_block()
            block_data = self.preset_blocks[-1]
            block_data['active_var'].set(block.get("active", True))
            block_data['role_var'].set(block.get("role", "system"))
            block_data['content_text'].delete("1.0", tk.END)
            block_data['content_text'].insert("1.0", block.get("content", ""))
        
        self.preset_name_entry.delete(0, tk.END)
        self.preset_name_entry.insert(0, preset_name)
        
        messagebox.showinfo("Success", f"Preset '{preset_name}' loaded!")
    
    def set_active_preset(self):
        """Set the selected preset as active"""
        preset_name = self.preset_list_var.get()
        if not preset_name:
            messagebox.showwarning("Warning", "Please select a preset")
            return
        
        self.config_manager.set_active_preset(preset_name)
        messagebox.showinfo("Success", f"Preset '{preset_name}' is now active!")
    
    def refresh_preset_list(self):
        """Refresh the preset dropdown list"""
        presets = self.config_manager.get_presets()
        preset_names = [p.get("name", "unknown") for p in presets]
        self.preset_list_dropdown['values'] = preset_names
        if preset_names:
            self.preset_list_var.set(preset_names[0])
    
    def create_user_characters_tab(self):
        """Create user characters management tab (similar to Characters tab)"""
        
        # Add User Character
        add_frame = ttk.LabelFrame(self.user_characters_frame, text="Add New User Character", padding=10)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Character Name (ID)
        ttk.Label(add_frame, text="Character Name (ID):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_char_name_entry = ttk.Entry(add_frame, width=30)
        self.user_char_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(lowercase, no spaces)", font=('TkDefaultFont', 8, 'italic')).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Display Name
        ttk.Label(add_frame, text="Display Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_char_display_name_entry = ttk.Entry(add_frame, width=30)
        self.user_char_display_name_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(shown in chat)", font=('TkDefaultFont', 8, 'italic')).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Description
        ttk.Label(add_frame, text="Description:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.user_char_description_text = scrolledtext.ScrolledText(add_frame, height=5, width=50)
        self.user_char_description_text.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(Character background/info)", font=('TkDefaultFont', 8, 'italic')).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Avatar selection
        avatar_frame = ttk.LabelFrame(add_frame, text="Avatar/Icon", padding=5)
        avatar_frame.grid(row=4, column=0, columnspan=3, sticky=tk.EW, pady=10, padx=5)
        
        # Avatar URL option
        ttk.Label(avatar_frame, text="Avatar URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_char_avatar_url_entry = ttk.Entry(avatar_frame, width=40)
        self.user_char_avatar_url_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        # OR separator
        ttk.Label(avatar_frame, text="--- OR ---").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Avatar file option
        ttk.Label(avatar_frame, text="Avatar File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_char_avatar_file_var = tk.StringVar()
        self.user_char_avatar_file_entry = ttk.Entry(avatar_frame, width=30, textvariable=self.user_char_avatar_file_var, state='readonly')
        self.user_char_avatar_file_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(avatar_frame, text="Browse...", command=self.browse_user_char_avatar_file).grid(row=2, column=2, pady=5, padx=5)
        
        ttk.Button(add_frame, text="Add User Character", command=self.add_user_character).grid(row=5, column=1, pady=10)
        
        # List User Characters
        list_frame = ttk.LabelFrame(self.user_characters_frame, text="Current User Characters", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_characters_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
        self.user_characters_listbox.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.LEFT)
        scrollbar.config(command=self.user_characters_listbox.yview)
        
        # Buttons for character management
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Refresh List", command=self.refresh_user_characters_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_user_character).pack(side=tk.LEFT, padx=5)
        
        self.refresh_user_characters_list()
    
    def browse_user_char_avatar_file(self):
        """Browse for user character avatar image file"""
        filename = filedialog.askopenfilename(
            title="Select Avatar Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.user_char_avatar_file_var.set(filename)
    
    def add_user_character(self):
        """Add a new user character"""
        name = self.user_char_name_entry.get().strip().lower().replace(" ", "_")
        display_name = self.user_char_display_name_entry.get().strip()
        description = self.user_char_description_text.get("1.0", tk.END).strip()
        avatar_url = self.user_char_avatar_url_entry.get().strip()
        avatar_file_source = self.user_char_avatar_file_var.get().strip()
        
        if not name or not display_name:
            messagebox.showerror("Error", "Please enter character name and display name")
            return
        
        try:
            # Handle avatar file if provided
            avatar_file_dest = ""
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Create avatars directory if it doesn't exist
                avatars_dir = "character_avatars"
                os.makedirs(avatars_dir, exist_ok=True)
                
                # Copy file to avatars directory with character name
                file_ext = os.path.splitext(avatar_file_source)[1]
                avatar_file_dest = os.path.join(avatars_dir, f"user_{name}{file_ext}")
                shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Add character to config
            self.config_manager.add_user_character(name, display_name, description, avatar_url, avatar_file_dest)
            
            # Clear form
            self.user_char_name_entry.delete(0, tk.END)
            self.user_char_display_name_entry.delete(0, tk.END)
            self.user_char_description_text.delete("1.0", tk.END)
            self.user_char_avatar_url_entry.delete(0, tk.END)
            self.user_char_avatar_file_var.set("")
            
            self.refresh_user_characters_list()
            messagebox.showinfo("Success", f"User character '{display_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user character: {str(e)}")
    
    def delete_user_character(self):
        """Delete selected user character"""
        selection = self.user_characters_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user character to delete")
            return
        
        index = selection[0]
        characters = self.config_manager.get_user_characters()
        if 0 <= index < len(characters):
            char_name = characters[index].get("display_name", characters[index].get("name", "Unknown"))
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user character '{char_name}'?"):
                try:
                    # Delete avatar file if it exists
                    avatar_file = characters[index].get("avatar_file", "")
                    if avatar_file and os.path.exists(avatar_file):
                        os.remove(avatar_file)
                    
                    self.config_manager.delete_user_character(index)
                    self.refresh_user_characters_list()
                    messagebox.showinfo("Success", f"User character '{char_name}' deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete user character: {str(e)}")
    
    def refresh_user_characters_list(self):
        """Refresh the user characters list"""
        self.user_characters_listbox.delete(0, tk.END)
        characters = self.config_manager.get_user_characters()
        for char in characters:
            display_name = char.get("display_name", char.get("name", "Unknown"))
            name_id = char.get("name", "unknown")
            description = char.get("description", "No description")
            desc_preview = description[:40] + "..." if len(description) > 40 else description
            self.user_characters_listbox.insert(tk.END, f"{display_name} ({name_id}): {desc_preview}")


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = PresetBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
