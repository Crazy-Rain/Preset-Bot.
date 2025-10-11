"""
Preset Bot - GUI Configuration and Manual Send Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import asyncio
import threading
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
        
        # Manual Send Tab
        self.manual_send_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manual_send_frame, text="Manual Send")
        self.create_manual_send_tab()
        
        # Characters Tab
        self.characters_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.characters_frame, text="Characters")
        self.create_characters_tab()
    
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
        
        ttk.Label(add_frame, text="Character Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.char_name_entry = ttk.Entry(add_frame, width=30)
        self.char_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(add_frame, text="System Prompt:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.char_prompt_text = scrolledtext.ScrolledText(add_frame, height=5, width=50)
        self.char_prompt_text.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Button(add_frame, text="Add Character", command=self.add_character).grid(row=2, column=1, pady=5)
        
        # List Characters
        list_frame = ttk.LabelFrame(self.characters_frame, text="Current Characters", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.characters_listbox = tk.Listbox(list_frame, height=10)
        self.characters_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(list_frame, text="Refresh List", command=self.refresh_characters_list).pack(pady=5)
        
        self.refresh_characters_list()
    
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
    
    def send_manual_message(self):
        """Send manual message through Discord bot"""
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
        
        self.send_status_label.config(text="Sending message...", foreground="blue")
        
        def send():
            try:
                # Get AI response
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                ai_response = loop.run_until_complete(
                    self.ai_handler.get_ai_response(message, character)
                )
                
                # Initialize Discord client if needed
                if not self.discord_client:
                    self.discord_client = discord.Client(intents=discord.Intents.default())
                    
                    @self.discord_client.event
                    async def on_ready():
                        try:
                            channel = self.discord_client.get_channel(int(channel_id))
                            if channel:
                                await channel.send(ai_response)
                                self.send_status_label.config(text=f"Message sent successfully!", foreground="green")
                                messagebox.showinfo("Success", f"Message sent to channel {channel_id}")
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
    
    def clear_message(self):
        """Clear message text"""
        self.message_text.delete("1.0", tk.END)
    
    def update_character_dropdown(self):
        """Update character dropdown with current characters"""
        characters = self.config_manager.get_characters()
        character_names = [char["name"] for char in characters]
        self.character_dropdown['values'] = character_names
        if character_names:
            self.character_var.set(character_names[0])
    
    def add_character(self):
        """Add a new character"""
        name = self.char_name_entry.get()
        prompt = self.char_prompt_text.get("1.0", tk.END).strip()
        
        if not name or not prompt:
            messagebox.showerror("Error", "Please enter both character name and system prompt")
            return
        
        try:
            self.config_manager.add_character(name, prompt)
            self.char_name_entry.delete(0, tk.END)
            self.char_prompt_text.delete("1.0", tk.END)
            self.refresh_characters_list()
            self.update_character_dropdown()
            messagebox.showinfo("Success", f"Character '{name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add character: {str(e)}")
    
    def refresh_characters_list(self):
        """Refresh the characters list"""
        self.characters_listbox.delete(0, tk.END)
        characters = self.config_manager.get_characters()
        for char in characters:
            self.characters_listbox.insert(tk.END, f"{char['name']}: {char['system_prompt'][:50]}...")
        self.update_character_dropdown()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = PresetBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
