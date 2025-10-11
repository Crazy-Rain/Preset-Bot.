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
import requests
from typing import Optional
from bot import ConfigManager, AIResponseHandler, split_text_intelligently
import discord
from PIL import Image, ImageTk
from io import BytesIO


class PresetBotGUI:
    """GUI for configuring the bot and sending manual messages"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Preset Discord Bot - Configuration & Manual Send")
        self.root.geometry("800x700")
        
        # Set up window close handler to prevent X11 errors
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.config_manager = ConfigManager()
        self.ai_handler = AIResponseHandler(self.config_manager)
        self.discord_client = None
        
        # Set up logging callback for AI handler
        self.ai_handler.set_log_callback(self.log_to_console)
        
        self.create_widgets()
        self.load_current_config()
    
    def upload_to_catbox(self, file_path: str) -> Optional[str]:
        """
        Upload an image file to catbox.moe and return the URL
        
        Args:
            file_path: Path to the image file to upload
            
        Returns:
            URL of the uploaded image, or None if upload failed
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'fileToUpload': f}
                data = {'reqtype': 'fileupload'}
                
                response = requests.post(
                    'https://catbox.moe/user/api.php',
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    url = response.text.strip()
                    if url.startswith('http'):
                        return url
                    else:
                        print(f"Catbox upload returned unexpected response: {url}")
                        return None
                else:
                    print(f"Catbox upload failed with status {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"Error uploading to catbox: {str(e)}")
            return None
    
    def validate_avatar_url(self, url: str) -> tuple[bool, str]:
        """
        Validate an avatar URL to check if it's accessible and suitable for Discord
        
        Args:
            url: The URL to validate
            
        Returns:
            Tuple of (is_valid, message) where message explains the result
        """
        if not url or not url.strip():
            return False, "URL is empty"
        
        url = url.strip()
        
        # Check if it's a valid URL format
        if not url.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"
        
        try:
            # Try to download the image header to check accessibility and size
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            # Check if URL is accessible
            if response.status_code != 200:
                return False, f"URL returned HTTP {response.status_code} - image may not be accessible"
            
            # Check content type
            content_type = response.headers.get('Content-Type', '').lower()
            valid_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
            
            if not any(t in content_type for t in valid_types):
                # Try GET request as some servers don't support HEAD
                response = requests.get(url, timeout=10, stream=True)
                if response.status_code != 200:
                    return False, f"URL returned HTTP {response.status_code} - image may not be accessible"
                content_type = response.headers.get('Content-Type', '').lower()
            
            if not any(t in content_type for t in valid_types):
                return False, f"Invalid image type. Must be PNG, JPG, GIF, or WEBP. Got: {content_type}"
            
            # Check content length (Discord has an 8MB limit for avatars, but recommend smaller)
            content_length = response.headers.get('Content-Length')
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                if size_mb > 8:
                    return False, f"Image is too large ({size_mb:.1f}MB). Discord supports up to 8MB, but smaller is recommended"
                elif size_mb > 2:
                    return True, f"⚠️ Image is large ({size_mb:.1f}MB). Smaller images load faster in Discord"
            
            return True, "✓ Avatar URL is valid and accessible"
            
        except requests.exceptions.Timeout:
            return False, "Request timed out - URL may be slow or inaccessible"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed - check if URL is correct and accessible"
        except Exception as e:
            return False, f"Error validating URL: {str(e)}"
    
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
        
        # Lorebooks Tab
        self.lorebooks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lorebooks_frame, text="Lorebooks")
        self.create_lorebooks_tab()
        
        # Console Tab
        self.console_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.console_frame, text="Console")
        self.create_console_tab()
    
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
        
        # Thinking Tags Configuration
        thinking_frame = ttk.LabelFrame(self.config_frame, text="Thinking Tags (Remove AI Internal Thoughts)", padding=10)
        thinking_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.thinking_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(thinking_frame, text="Enable Thinking Tag Removal", variable=self.thinking_enabled_var).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Label(thinking_frame, text="Start Tag:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.thinking_start_tag_entry = ttk.Entry(thinking_frame, width=20)
        self.thinking_start_tag_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        self.thinking_start_tag_entry.insert(0, "<think>")
        ttk.Label(thinking_frame, text="(e.g., <think>, <thinking>)", font=('TkDefaultFont', 8, 'italic')).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(thinking_frame, text="End Tag:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.thinking_end_tag_entry = ttk.Entry(thinking_frame, width=20)
        self.thinking_end_tag_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.thinking_end_tag_entry.insert(0, "</think>")
        ttk.Label(thinking_frame, text="(e.g., </think>, </thinking>)", font=('TkDefaultFont', 8, 'italic')).grid(row=2, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(thinking_frame, text="Content between these tags will be removed from AI responses before sending to Discord.", 
                 font=('TkDefaultFont', 8, 'italic'), wraplength=600).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Chat History Configuration
        chat_frame = ttk.LabelFrame(self.config_frame, text="Chat History Settings", padding=10)
        chat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(chat_frame, text="Message History Limit:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.chat_history_limit_entry = ttk.Entry(chat_frame, width=10)
        self.chat_history_limit_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        self.chat_history_limit_entry.insert(0, "20")
        ttk.Label(chat_frame, text="messages (how far back to include in AI context)", 
                 font=('TkDefaultFont', 8, 'italic')).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(chat_frame, text="Higher values allow AI to remember more conversation history but use more tokens.", 
                 font=('TkDefaultFont', 8, 'italic'), wraplength=600).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
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
        
        # Add/Edit Character
        add_frame = ttk.LabelFrame(self.characters_frame, text="Add/Edit Character", padding=10)
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
        self.char_description_text = scrolledtext.ScrolledText(add_frame, height=4, width=50)
        self.char_description_text.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(AI system prompt)", font=('TkDefaultFont', 8, 'italic')).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Scenario
        ttk.Label(add_frame, text="Scenario:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.char_scenario_text = scrolledtext.ScrolledText(add_frame, height=3, width=50)
        self.char_scenario_text.grid(row=4, column=1, columnspan=2, pady=5, padx=5, sticky=tk.W)
        ttk.Label(add_frame, text="(Default situation/scenario for this character)", font=('TkDefaultFont', 8, 'italic')).grid(row=5, column=1, sticky=tk.W, padx=5)
        
        # Avatar selection
        avatar_frame = ttk.LabelFrame(add_frame, text="Avatar/Icon", padding=5)
        avatar_frame.grid(row=6, column=0, columnspan=3, sticky=tk.EW, pady=10, padx=5)
        
        # Avatar URL option
        ttk.Label(avatar_frame, text="Avatar URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.char_avatar_url_entry = ttk.Entry(avatar_frame, width=40)
        self.char_avatar_url_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(avatar_frame, text="Test URL", command=self.test_char_avatar_url).grid(row=0, column=2, pady=5, padx=5)
        
        # OR separator
        ttk.Label(avatar_frame, text="--- OR ---").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Avatar file option
        ttk.Label(avatar_frame, text="Avatar File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.char_avatar_file_var = tk.StringVar()
        self.char_avatar_file_entry = ttk.Entry(avatar_frame, width=30, textvariable=self.char_avatar_file_var, state='readonly')
        self.char_avatar_file_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(avatar_frame, text="Browse...", command=self.browse_avatar_file).grid(row=2, column=2, pady=5, padx=5)
        
        # Upload to catbox option
        self.char_upload_to_catbox_var = tk.BooleanVar(value=False)
        self.char_upload_to_catbox_cb = ttk.Checkbutton(avatar_frame, text="Upload to catbox.moe (for avatar URL)", variable=self.char_upload_to_catbox_var)
        self.char_upload_to_catbox_cb.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Avatar Preview section
        preview_frame = ttk.LabelFrame(add_frame, text="Avatar Preview", padding=5)
        preview_frame.grid(row=0, column=3, rowspan=7, sticky=tk.N, padx=10, pady=5)
        
        # Preview label for image
        self.char_avatar_preview_label = ttk.Label(preview_frame, text="No avatar loaded", relief=tk.SUNKEN, width=20)
        self.char_avatar_preview_label.pack(pady=5)
        
        # Preview button to load/refresh preview
        ttk.Button(preview_frame, text="Load Preview", command=self.load_char_avatar_preview).pack(pady=5)
        
        # Store the preview image to prevent garbage collection
        self.char_avatar_preview_image = None
        
        # Action buttons
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=7, column=1, pady=10)
        ttk.Button(button_frame, text="Add Character", command=self.add_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Selected", command=self.update_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_character_form).pack(side=tk.LEFT, padx=5)
        
        # Store editing index
        self.char_editing_index = None
        
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
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_character).pack(side=tk.LEFT, padx=5)
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
    
    def test_char_avatar_url(self):
        """Test character avatar URL for validity and accessibility"""
        url = self.char_avatar_url_entry.get().strip()
        
        if not url:
            messagebox.showinfo("Test Avatar URL", "Please enter an Avatar URL to test")
            return
        
        # Show testing message
        test_window = tk.Toplevel(self.root)
        test_window.title("Testing Avatar URL")
        test_window.geometry("300x100")
        ttk.Label(test_window, text="Testing avatar URL...", padding=20).pack()
        test_window.update()
        
        # Validate the URL
        is_valid, message = self.validate_avatar_url(url)
        
        # Close testing window
        test_window.destroy()
        
        # Show result
        if is_valid:
            messagebox.showinfo("Avatar URL Test", message)
        else:
            messagebox.showerror("Avatar URL Test Failed", message)
    
    def load_char_avatar_preview(self):
        """Load and display character avatar preview"""
        # Get URL from entry or file path
        url = self.char_avatar_url_entry.get().strip()
        file_path = self.char_avatar_file_var.get().strip()
        
        image_source = url if url else file_path
        
        if not image_source:
            messagebox.showinfo("Avatar Preview", "Please enter an Avatar URL or select an avatar file first")
            return
        
        try:
            # Load image from URL or file
            if url:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    image = Image.open(image_data)
                else:
                    messagebox.showerror("Preview Error", f"Failed to load image from URL (HTTP {response.status_code})")
                    return
            else:
                if os.path.exists(file_path):
                    image = Image.open(file_path)
                else:
                    messagebox.showerror("Preview Error", "File does not exist")
                    return
            
            # Resize image to fit preview (128x128 max)
            image.thumbnail((128, 128), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update label with image
            self.char_avatar_preview_label.configure(image=photo, text="")
            self.char_avatar_preview_image = photo  # Keep reference to prevent garbage collection
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error loading image: {str(e)}")
    
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
        
        # Thinking Tags Configuration
        thinking_config = self.config_manager.get_thinking_tags_config()
        self.thinking_enabled_var.set(thinking_config.get("enabled", False))
        self.thinking_start_tag_entry.delete(0, tk.END)
        self.thinking_start_tag_entry.insert(0, thinking_config.get("start_tag", "<think>"))
        self.thinking_end_tag_entry.delete(0, tk.END)
        self.thinking_end_tag_entry.insert(0, thinking_config.get("end_tag", "</think>"))
        
        # Chat History Limit
        chat_limit = self.config_manager.get_chat_history_limit()
        self.chat_history_limit_entry.delete(0, tk.END)
        self.chat_history_limit_entry.insert(0, str(chat_limit))
        
        # AI Configuration Options
        try:
            ai_config = self.config_manager.get_ai_config_options()
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
            if reasoning_level in ['Auto', 'Maximum', 'High', 'Medium', 'Low', 'Minimum']:
                self.preset_reasoning_level.set(reasoning_level)
            
            self.preset_use_presence_penalty.set(ai_config.get("use_presence_penalty", False))
            self.preset_presence_penalty.delete(0, tk.END)
            self.preset_presence_penalty.insert(0, str(ai_config.get("presence_penalty", 0.0)))
            
            self.preset_use_frequency_penalty.set(ai_config.get("use_frequency_penalty", False))
            self.preset_frequency_penalty.delete(0, tk.END)
            self.preset_frequency_penalty.insert(0, str(ai_config.get("frequency_penalty", 0.0)))
        except (AttributeError, KeyError):
            # If AI config fields don't exist, skip loading them
            pass
        
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
            
            # Save thinking tags configuration
            thinking_enabled = self.thinking_enabled_var.get()
            thinking_start_tag = self.thinking_start_tag_entry.get()
            thinking_end_tag = self.thinking_end_tag_entry.get()
            self.config_manager.set_thinking_tags_config(thinking_enabled, thinking_start_tag, thinking_end_tag)
            
            # Save chat history limit
            try:
                chat_limit = int(self.chat_history_limit_entry.get())
                if chat_limit < 1:
                    raise ValueError("Chat history limit must be at least 1")
                self.config_manager.set_chat_history_limit(chat_limit)
            except ValueError as e:
                messagebox.showerror("Invalid Input", f"Chat history limit must be a positive integer: {str(e)}")
                return
            
            # Save AI configuration options
            try:
                ai_config_options = {
                    "max_tokens": int(self.preset_max_tokens.get()),
                    "response_length": int(self.preset_response_length.get()),
                    "temperature": float(self.preset_temperature.get()),
                    "top_p": float(self.preset_top_p.get()),
                    "reasoning_enabled": self.preset_reasoning_var.get(),
                    "reasoning_level": self.preset_reasoning_level.get(),
                    "use_presence_penalty": self.preset_use_presence_penalty.get(),
                    "presence_penalty": float(self.preset_presence_penalty.get()),
                    "use_frequency_penalty": self.preset_use_frequency_penalty.get(),
                    "frequency_penalty": float(self.preset_frequency_penalty.get())
                }
                self.config_manager.set_ai_config_options(ai_config_options)
            except (ValueError, AttributeError):
                # If AI config fields don't exist or have invalid values, skip saving them
                pass
            
            self.config_status_label.config(text="Configuration saved successfully!", foreground="green")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            self.config_status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def test_openai(self):
        """Test OpenAI connection"""
        self.config_status_label.config(text="Testing OpenAI connection...", foreground="blue")
        self.log_to_console("Testing OpenAI connection...", 'info')
        
        def test():
            try:
                # Save current config first
                base_url = self.openai_base_url_entry.get()
                api_key = self.openai_api_key_entry.get()
                if base_url and api_key:
                    self.config_manager.set_openai_config(base_url, api_key)
                    self.ai_handler.update_client()
                
                self.log_to_console(f"Sending test request to {base_url}", 'request')
                
                # Test with a simple message
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    self.ai_handler.get_ai_response("Say 'Connection successful!'")
                )
                loop.close()
                
                if "Error" not in response:
                    self.config_status_label.config(text="OpenAI connection successful!", foreground="green")
                    self.log_to_console(f"Response received: {response[:200]}...", 'response')
                    messagebox.showinfo("Success", f"Connection successful!\nResponse: {response[:100]}...")
                else:
                    self.config_status_label.config(text="Connection failed", foreground="red")
                    self.log_to_console(f"Error response: {response}", 'error')
                    messagebox.showerror("Error", response)
            except Exception as e:
                self.config_status_label.config(text=f"Error: {str(e)}", foreground="red")
                self.log_to_console(f"Connection failed: {str(e)}", 'error')
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
        self.log_to_console(f"Preparing to send manual message to channel {channel_id} as {character}", 'info')
        
        def send():
            try:
                # Reload config to get latest character updates
                self.config_manager.reload_config()
                
                # Get character data
                char_data = self.config_manager.get_character_by_name(character)
                if not char_data:
                    self.send_status_label.config(text="Character not found", foreground="red")
                    self.log_to_console(f"Character '{character}' not found", 'error')
                    messagebox.showerror("Error", f"Character '{character}' not found")
                    return
                
                # Skip AI processing - send message directly
                # The message is sent as-is from the selected character
                self.log_to_console(f"Message content: {message[:200]}...", 'info')
                
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
                                self.log_to_console(f"Message sent successfully to channel {channel_id} as {char_data.get('display_name', character)}", 'info')
                                messagebox.showinfo("Success", f"Message sent to channel {channel_id} as {char_data.get('display_name', character)}")
                            else:
                                self.send_status_label.config(text="Channel not found", foreground="red")
                                self.log_to_console(f"Channel {channel_id} not found", 'error')
                                messagebox.showerror("Error", f"Channel {channel_id} not found")
                        except Exception as e:
                            self.send_status_label.config(text=f"Error: {str(e)}", foreground="red")
                            self.log_to_console(f"Failed to send message: {str(e)}", 'error')
                            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
                        finally:
                            await self.discord_client.close()
                    
                    token = self.config_manager.get_discord_token()
                    if not token:
                        self.send_status_label.config(text="Discord token not configured", foreground="red")
                        self.log_to_console("Discord token not configured", 'error')
                        messagebox.showerror("Error", "Please configure Discord bot token first")
                        return
                    
                    loop.run_until_complete(self.discord_client.start(token))
                    self.discord_client = None
                
                loop.close()
            except Exception as e:
                self.send_status_label.config(text=f"Error: {str(e)}", foreground="red")
                self.log_to_console(f"Failed to send message: {str(e)}", 'error')
                messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        
        threading.Thread(target=send, daemon=True).start()
    
    async def send_via_webhook(self, channel, content: str, character: dict) -> None:
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
            except Exception as e:
                self.log_to_console(f"Failed to load avatar file: {str(e)}", 'error')
        
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
            
            self.log_to_console(f"Message split into {len(chunks)} chunks due to length", 'info')
    
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
        scenario = self.char_scenario_text.get("1.0", tk.END).strip()
        avatar_url = self.char_avatar_url_entry.get().strip()
        avatar_file_source = self.char_avatar_file_var.get().strip()
        
        if not name or not display_name or not description:
            messagebox.showerror("Error", "Please enter character name, display name, and description")
            return
        
        try:
            # Validate avatar URL if provided (and no file is being uploaded)
            if avatar_url and not avatar_file_source:
                is_valid, validation_msg = self.validate_avatar_url(avatar_url)
                if not is_valid:
                    result = messagebox.askyesno(
                        "Avatar URL Validation Failed", 
                        f"{validation_msg}\n\nDo you want to continue anyway?"
                    )
                    if not result:
                        return
                elif "⚠️" in validation_msg:
                    # Show warning but don't block
                    messagebox.showwarning("Avatar URL Warning", validation_msg)
            
            # Handle avatar file if provided
            avatar_file_dest = ""
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Check if user wants to upload to catbox.moe
                if self.char_upload_to_catbox_var.get():
                    # Upload to catbox.moe
                    messagebox.showinfo("Uploading", "Uploading avatar to catbox.moe...")
                    uploaded_url = self.upload_to_catbox(avatar_file_source)
                    
                    if uploaded_url:
                        # Use the uploaded URL as avatar_url
                        avatar_url = uploaded_url
                        messagebox.showinfo("Success", f"Avatar uploaded successfully!\nURL: {uploaded_url}")
                        
                        # Still copy locally as backup
                        avatars_dir = "character_avatars"
                        os.makedirs(avatars_dir, exist_ok=True)
                        file_ext = os.path.splitext(avatar_file_source)[1]
                        avatar_file_dest = os.path.join(avatars_dir, f"{name}{file_ext}")
                        shutil.copy2(avatar_file_source, avatar_file_dest)
                    else:
                        messagebox.showwarning("Upload Failed", "Failed to upload avatar to catbox.moe. The character will be created without an avatar URL.")
                else:
                    # Just copy locally without uploading
                    avatars_dir = "character_avatars"
                    os.makedirs(avatars_dir, exist_ok=True)
                    file_ext = os.path.splitext(avatar_file_source)[1]
                    avatar_file_dest = os.path.join(avatars_dir, f"{name}{file_ext}")
                    shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Add character to config
            self.config_manager.add_character(name, display_name, description, avatar_url, avatar_file_dest, scenario)
            
            # Clear form
            self.clear_character_form()
            
            self.refresh_characters_list()
            self.update_character_dropdown()
            messagebox.showinfo("Success", f"Character '{display_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add character: {str(e)}")
    
    def update_character(self):
        """Update selected character"""
        if self.char_editing_index is None:
            messagebox.showwarning("Warning", "Please select a character to edit first using 'Edit Selected' button")
            return
        
        name = self.char_name_entry.get().strip().lower().replace(" ", "_")
        display_name = self.char_display_name_entry.get().strip()
        description = self.char_description_text.get("1.0", tk.END).strip()
        scenario = self.char_scenario_text.get("1.0", tk.END).strip()
        avatar_url = self.char_avatar_url_entry.get().strip()
        avatar_file_source = self.char_avatar_file_var.get().strip()
        
        if not name or not display_name or not description:
            messagebox.showerror("Error", "Please enter character name, display name, and description")
            return
        
        try:
            # Validate avatar URL if provided (and no file is being uploaded)
            characters = self.config_manager.get_characters()
            current_avatar_url = characters[self.char_editing_index].get("avatar_url", "")
            
            if avatar_url and avatar_url != current_avatar_url and not avatar_file_source:
                is_valid, validation_msg = self.validate_avatar_url(avatar_url)
                if not is_valid:
                    result = messagebox.askyesno(
                        "Avatar URL Validation Failed", 
                        f"{validation_msg}\n\nDo you want to continue anyway?"
                    )
                    if not result:
                        return
                elif "⚠️" in validation_msg:
                    # Show warning but don't block
                    messagebox.showwarning("Avatar URL Warning", validation_msg)
            
            # Handle avatar file if provided
            current_avatar_file = characters[self.char_editing_index].get("avatar_file", "")
            current_avatar_url = characters[self.char_editing_index].get("avatar_url", "")
            avatar_file_dest = current_avatar_file
            
            # Check if a new file was selected (different from stored path, not comparing actual files)
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Check if user wants to upload to catbox.moe
                if self.char_upload_to_catbox_var.get():
                    # Only upload if it's a different file or if there's no current avatar URL
                    should_upload = (avatar_file_source != current_avatar_file) or not current_avatar_url
                    
                    if should_upload:
                        # Upload to catbox.moe
                        messagebox.showinfo("Uploading", "Uploading avatar to catbox.moe...")
                        uploaded_url = self.upload_to_catbox(avatar_file_source)
                        
                        if uploaded_url:
                            # Use the uploaded URL as avatar_url
                            avatar_url = uploaded_url
                            messagebox.showinfo("Success", f"Avatar uploaded successfully!\nURL: {uploaded_url}")
                            
                            # Still copy locally as backup
                            avatars_dir = "character_avatars"
                            os.makedirs(avatars_dir, exist_ok=True)
                            file_ext = os.path.splitext(avatar_file_source)[1]
                            avatar_file_dest = os.path.join(avatars_dir, f"{name}{file_ext}")
                            shutil.copy2(avatar_file_source, avatar_file_dest)
                        else:
                            messagebox.showwarning("Upload Failed", "Failed to upload avatar to catbox.moe. Keeping existing avatar URL.")
                            # Keep existing URL if upload fails
                            if not avatar_url:
                                avatar_url = current_avatar_url
                    else:
                        # File hasn't changed and we already have a URL, keep existing values
                        if not avatar_url:
                            avatar_url = current_avatar_url
                else:
                    # Just copy locally without uploading
                    if avatar_file_source != current_avatar_file:
                        avatars_dir = "character_avatars"
                        os.makedirs(avatars_dir, exist_ok=True)
                        file_ext = os.path.splitext(avatar_file_source)[1]
                        avatar_file_dest = os.path.join(avatars_dir, f"{name}{file_ext}")
                        shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Update character in config
            self.config_manager.update_character(self.char_editing_index, name, display_name, description, avatar_url, avatar_file_dest, scenario)
            
            # Clear form and editing state
            self.clear_character_form()
            self.char_editing_index = None
            
            self.refresh_characters_list()
            self.update_character_dropdown()
            messagebox.showinfo("Success", f"Character '{display_name}' updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update character: {str(e)}")
    
    def edit_character(self):
        """Load selected character into form for editing"""
        selection = self.characters_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a character to edit")
            return
        
        index = selection[0]
        characters = self.config_manager.get_characters()
        if 0 <= index < len(characters):
            char = characters[index]
            
            # Load character data into form
            self.char_name_entry.delete(0, tk.END)
            self.char_name_entry.insert(0, char.get("name", ""))
            
            self.char_display_name_entry.delete(0, tk.END)
            self.char_display_name_entry.insert(0, char.get("display_name", ""))
            
            self.char_description_text.delete("1.0", tk.END)
            self.char_description_text.insert("1.0", char.get("description", ""))
            
            self.char_scenario_text.delete("1.0", tk.END)
            self.char_scenario_text.insert("1.0", char.get("scenario", ""))
            
            self.char_avatar_url_entry.delete(0, tk.END)
            self.char_avatar_url_entry.insert(0, char.get("avatar_url", ""))
            
            self.char_avatar_file_var.set(char.get("avatar_file", ""))
            
            # Set editing index
            self.char_editing_index = index
            
            messagebox.showinfo("Edit Mode", f"Editing character '{char.get('display_name', char.get('name'))}'. Click 'Update Selected' to save changes.")
    
    def clear_character_form(self):
        """Clear the character form"""
        self.char_name_entry.delete(0, tk.END)
        self.char_display_name_entry.delete(0, tk.END)
        self.char_description_text.delete("1.0", tk.END)
        self.char_scenario_text.delete("1.0", tk.END)
        self.char_avatar_url_entry.delete(0, tk.END)
        self.char_avatar_file_var.set("")
        self.char_upload_to_catbox_var.set(False)
        self.char_editing_index = None
    
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
        
        # Add/Edit User Character
        add_frame = ttk.LabelFrame(self.user_characters_frame, text="Add/Edit User Character", padding=10)
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
        ttk.Button(avatar_frame, text="Test URL", command=self.test_user_char_avatar_url).grid(row=0, column=2, pady=5, padx=5)
        
        # OR separator
        ttk.Label(avatar_frame, text="--- OR ---").grid(row=1, column=0, columnspan=2, pady=5)
        
        # Avatar file option
        ttk.Label(avatar_frame, text="Avatar File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_char_avatar_file_var = tk.StringVar()
        self.user_char_avatar_file_entry = ttk.Entry(avatar_frame, width=30, textvariable=self.user_char_avatar_file_var, state='readonly')
        self.user_char_avatar_file_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(avatar_frame, text="Browse...", command=self.browse_user_char_avatar_file).grid(row=2, column=2, pady=5, padx=5)
        
        # Upload to catbox option
        self.user_char_upload_to_catbox_var = tk.BooleanVar(value=False)
        self.user_char_upload_to_catbox_cb = ttk.Checkbutton(avatar_frame, text="Upload to catbox.moe (for avatar URL)", variable=self.user_char_upload_to_catbox_var)
        self.user_char_upload_to_catbox_cb.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Avatar Preview section
        preview_frame = ttk.LabelFrame(add_frame, text="Avatar Preview", padding=5)
        preview_frame.grid(row=0, column=3, rowspan=5, sticky=tk.N, padx=10, pady=5)
        
        # Preview label for image
        self.user_char_avatar_preview_label = ttk.Label(preview_frame, text="No avatar loaded", relief=tk.SUNKEN, width=20)
        self.user_char_avatar_preview_label.pack(pady=5)
        
        # Preview button to load/refresh preview
        ttk.Button(preview_frame, text="Load Preview", command=self.load_user_char_avatar_preview).pack(pady=5)
        
        # Store the preview image to prevent garbage collection
        self.user_char_avatar_preview_image = None
        
        # Action buttons
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=5, column=1, pady=10)
        ttk.Button(button_frame, text="Add User Character", command=self.add_user_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Selected", command=self.update_user_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_user_character_form).pack(side=tk.LEFT, padx=5)
        
        # Store editing index
        self.user_char_editing_index = None
        
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
        ttk.Button(button_frame, text="Edit Selected", command=self.edit_user_character).pack(side=tk.LEFT, padx=5)
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
    
    def test_user_char_avatar_url(self):
        """Test user character avatar URL for validity and accessibility"""
        url = self.user_char_avatar_url_entry.get().strip()
        
        if not url:
            messagebox.showinfo("Test Avatar URL", "Please enter an Avatar URL to test")
            return
        
        # Show testing message
        test_window = tk.Toplevel(self.root)
        test_window.title("Testing Avatar URL")
        test_window.geometry("300x100")
        ttk.Label(test_window, text="Testing avatar URL...", padding=20).pack()
        test_window.update()
        
        # Validate the URL
        is_valid, message = self.validate_avatar_url(url)
        
        # Close testing window
        test_window.destroy()
        
        # Show result
        if is_valid:
            messagebox.showinfo("Avatar URL Test", message)
        else:
            messagebox.showerror("Avatar URL Test Failed", message)
    
    def load_user_char_avatar_preview(self):
        """Load and display user character avatar preview"""
        # Get URL from entry or file path
        url = self.user_char_avatar_url_entry.get().strip()
        file_path = self.user_char_avatar_file_var.get().strip()
        
        image_source = url if url else file_path
        
        if not image_source:
            messagebox.showinfo("Avatar Preview", "Please enter an Avatar URL or select an avatar file first")
            return
        
        try:
            # Load image from URL or file
            if url:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    image = Image.open(image_data)
                else:
                    messagebox.showerror("Preview Error", f"Failed to load image from URL (HTTP {response.status_code})")
                    return
            else:
                if os.path.exists(file_path):
                    image = Image.open(file_path)
                else:
                    messagebox.showerror("Preview Error", "File does not exist")
                    return
            
            # Resize image to fit preview (128x128 max)
            image.thumbnail((128, 128), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update label with image
            self.user_char_avatar_preview_label.configure(image=photo, text="")
            self.user_char_avatar_preview_image = photo  # Keep reference to prevent garbage collection
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error loading image: {str(e)}")
    
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
            # Validate avatar URL if provided (and no file is being uploaded)
            if avatar_url and not avatar_file_source:
                is_valid, validation_msg = self.validate_avatar_url(avatar_url)
                if not is_valid:
                    result = messagebox.askyesno(
                        "Avatar URL Validation Failed", 
                        f"{validation_msg}\n\nDo you want to continue anyway?"
                    )
                    if not result:
                        return
                elif "⚠️" in validation_msg:
                    # Show warning but don't block
                    messagebox.showwarning("Avatar URL Warning", validation_msg)
            
            # Handle avatar file if provided
            avatar_file_dest = ""
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Check if user wants to upload to catbox.moe
                if self.user_char_upload_to_catbox_var.get():
                    # Upload to catbox.moe
                    messagebox.showinfo("Uploading", "Uploading avatar to catbox.moe...")
                    uploaded_url = self.upload_to_catbox(avatar_file_source)
                    
                    if uploaded_url:
                        # Use the uploaded URL as avatar_url
                        avatar_url = uploaded_url
                        messagebox.showinfo("Success", f"Avatar uploaded successfully!\nURL: {uploaded_url}")
                        
                        # Still copy locally as backup
                        avatars_dir = "character_avatars"
                        os.makedirs(avatars_dir, exist_ok=True)
                        file_ext = os.path.splitext(avatar_file_source)[1]
                        avatar_file_dest = os.path.join(avatars_dir, f"user_{name}{file_ext}")
                        shutil.copy2(avatar_file_source, avatar_file_dest)
                    else:
                        messagebox.showwarning("Upload Failed", "Failed to upload avatar to catbox.moe. The character will be created without an avatar URL.")
                else:
                    # Just copy locally without uploading
                    avatars_dir = "character_avatars"
                    os.makedirs(avatars_dir, exist_ok=True)
                    file_ext = os.path.splitext(avatar_file_source)[1]
                    avatar_file_dest = os.path.join(avatars_dir, f"user_{name}{file_ext}")
                    shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Add character to config
            self.config_manager.add_user_character(name, display_name, description, avatar_url, avatar_file_dest)
            
            # Clear form
            self.clear_user_character_form()
            
            self.refresh_user_characters_list()
            messagebox.showinfo("Success", f"User character '{display_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user character: {str(e)}")
    
    def update_user_character(self):
        """Update selected user character"""
        if self.user_char_editing_index is None:
            messagebox.showwarning("Warning", "Please select a user character to edit first using 'Edit Selected' button")
            return
        
        name = self.user_char_name_entry.get().strip().lower().replace(" ", "_")
        display_name = self.user_char_display_name_entry.get().strip()
        description = self.user_char_description_text.get("1.0", tk.END).strip()
        avatar_url = self.user_char_avatar_url_entry.get().strip()
        avatar_file_source = self.user_char_avatar_file_var.get().strip()
        
        if not name or not display_name:
            messagebox.showerror("Error", "Please enter character name and display name")
            return
        
        try:
            # Validate avatar URL if provided (and no file is being uploaded)
            characters = self.config_manager.get_user_characters()
            current_avatar_url = characters[self.user_char_editing_index].get("avatar_url", "")
            
            if avatar_url and avatar_url != current_avatar_url and not avatar_file_source:
                is_valid, validation_msg = self.validate_avatar_url(avatar_url)
                if not is_valid:
                    result = messagebox.askyesno(
                        "Avatar URL Validation Failed", 
                        f"{validation_msg}\n\nDo you want to continue anyway?"
                    )
                    if not result:
                        return
                elif "⚠️" in validation_msg:
                    # Show warning but don't block
                    messagebox.showwarning("Avatar URL Warning", validation_msg)
            
            # Handle avatar file if provided
            current_avatar_file = characters[self.user_char_editing_index].get("avatar_file", "")
            current_avatar_url = characters[self.user_char_editing_index].get("avatar_url", "")
            avatar_file_dest = current_avatar_file
            
            # Check if a new file was selected (different from stored path, not comparing actual files)
            if avatar_file_source and os.path.exists(avatar_file_source):
                # Check if user wants to upload to catbox.moe
                if self.user_char_upload_to_catbox_var.get():
                    # Only upload if it's a different file or if there's no current avatar URL
                    should_upload = (avatar_file_source != current_avatar_file) or not current_avatar_url
                    
                    if should_upload:
                        # Upload to catbox.moe
                        messagebox.showinfo("Uploading", "Uploading avatar to catbox.moe...")
                        uploaded_url = self.upload_to_catbox(avatar_file_source)
                        
                        if uploaded_url:
                            # Use the uploaded URL as avatar_url
                            avatar_url = uploaded_url
                            messagebox.showinfo("Success", f"Avatar uploaded successfully!\nURL: {uploaded_url}")
                            
                            # Still copy locally as backup
                            avatars_dir = "character_avatars"
                            os.makedirs(avatars_dir, exist_ok=True)
                            file_ext = os.path.splitext(avatar_file_source)[1]
                            avatar_file_dest = os.path.join(avatars_dir, f"user_{name}{file_ext}")
                            shutil.copy2(avatar_file_source, avatar_file_dest)
                        else:
                            messagebox.showwarning("Upload Failed", "Failed to upload avatar to catbox.moe. Keeping existing avatar URL.")
                            # Keep existing URL if upload fails
                            if not avatar_url:
                                avatar_url = current_avatar_url
                    else:
                        # File hasn't changed and we already have a URL, keep existing values
                        if not avatar_url:
                            avatar_url = current_avatar_url
                else:
                    # Just copy locally without uploading
                    if avatar_file_source != current_avatar_file:
                        avatars_dir = "character_avatars"
                        os.makedirs(avatars_dir, exist_ok=True)
                        file_ext = os.path.splitext(avatar_file_source)[1]
                        avatar_file_dest = os.path.join(avatars_dir, f"user_{name}{file_ext}")
                        shutil.copy2(avatar_file_source, avatar_file_dest)
            
            # Update character in config
            self.config_manager.update_user_character(self.user_char_editing_index, name, display_name, description, avatar_url, avatar_file_dest)
            
            # Clear form and editing state
            self.clear_user_character_form()
            self.user_char_editing_index = None
            
            self.refresh_user_characters_list()
            messagebox.showinfo("Success", f"User character '{display_name}' updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user character: {str(e)}")
    
    def edit_user_character(self):
        """Load selected user character into form for editing"""
        selection = self.user_characters_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user character to edit")
            return
        
        index = selection[0]
        characters = self.config_manager.get_user_characters()
        if 0 <= index < len(characters):
            char = characters[index]
            
            # Load character data into form
            self.user_char_name_entry.delete(0, tk.END)
            self.user_char_name_entry.insert(0, char.get("name", ""))
            
            self.user_char_display_name_entry.delete(0, tk.END)
            self.user_char_display_name_entry.insert(0, char.get("display_name", ""))
            
            self.user_char_description_text.delete("1.0", tk.END)
            self.user_char_description_text.insert("1.0", char.get("description", ""))
            
            self.user_char_avatar_url_entry.delete(0, tk.END)
            self.user_char_avatar_url_entry.insert(0, char.get("avatar_url", ""))
            
            self.user_char_avatar_file_var.set(char.get("avatar_file", ""))
            
            # Set editing index
            self.user_char_editing_index = index
            
            messagebox.showinfo("Edit Mode", f"Editing user character '{char.get('display_name', char.get('name'))}'. Click 'Update Selected' to save changes.")
    
    def clear_user_character_form(self):
        """Clear the user character form"""
        self.user_char_name_entry.delete(0, tk.END)
        self.user_char_display_name_entry.delete(0, tk.END)
        self.user_char_description_text.delete("1.0", tk.END)
        self.user_char_avatar_url_entry.delete(0, tk.END)
        self.user_char_avatar_file_var.set("")
        self.user_char_upload_to_catbox_var.set(False)
        self.user_char_editing_index = None
    
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
    
    def create_lorebooks_tab(self):
        """Create lorebooks management tab"""
        
        # Main container with horizontal split
        main_paned = ttk.PanedWindow(self.lorebooks_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Lorebook list
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Lorebook management
        lorebook_mgmt_frame = ttk.LabelFrame(left_frame, text="Lorebook Management", padding=10)
        lorebook_mgmt_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add lorebook section
        add_lb_frame = ttk.Frame(lorebook_mgmt_frame)
        add_lb_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_lb_frame, text="New Lorebook:").pack(side=tk.LEFT, padx=5)
        self.lorebook_name_entry = ttk.Entry(add_lb_frame, width=20)
        self.lorebook_name_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(add_lb_frame, text="Create", command=self.add_lorebook).pack(side=tk.LEFT, padx=5)
        
        # Lorebook list
        list_frame = ttk.Frame(lorebook_mgmt_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lorebooks_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
        self.lorebooks_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=self.lorebooks_listbox.yview)
        self.lorebooks_listbox.bind('<<ListboxSelect>>', self.on_lorebook_select)
        
        # Lorebook action buttons
        lb_button_frame = ttk.Frame(lorebook_mgmt_frame)
        lb_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(lb_button_frame, text="Activate", command=self.activate_lorebook).pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Deactivate", command=self.deactivate_lorebook).pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Delete", command=self.delete_lorebook).pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Refresh", command=self.refresh_lorebooks_list).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Entry management
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # Entry management
        entry_mgmt_frame = ttk.LabelFrame(right_frame, text="Entry Management", padding=10)
        entry_mgmt_frame.pack(fill=tk.BOTH, expand=True)
        
        # Selected lorebook label
        self.selected_lorebook_label = ttk.Label(entry_mgmt_frame, text="No lorebook selected", 
                                                  font=('TkDefaultFont', 10, 'bold'))
        self.selected_lorebook_label.pack(pady=5)
        
        # Add/Edit Entry section
        entry_edit_frame = ttk.LabelFrame(entry_mgmt_frame, text="Add/Edit Entry", padding=10)
        entry_edit_frame.pack(fill=tk.X, pady=5)
        
        # Entry content
        ttk.Label(entry_edit_frame, text="Content:").grid(row=0, column=0, sticky=tk.NW, pady=5)
        self.entry_content_text = scrolledtext.ScrolledText(entry_edit_frame, height=4, width=50)
        self.entry_content_text.grid(row=0, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        # Activation type
        ttk.Label(entry_edit_frame, text="Activation Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_activation_type = tk.StringVar(value="normal")
        type_frame = ttk.Frame(entry_edit_frame)
        type_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(type_frame, text="Constant (Always Active)", variable=self.entry_activation_type, 
                       value="constant", command=self.on_activation_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Normal (Keyword Triggered)", variable=self.entry_activation_type, 
                       value="normal", command=self.on_activation_type_change).pack(anchor=tk.W)
        
        # Keywords (for normal entries)
        self.keywords_label = ttk.Label(entry_edit_frame, text="Keywords:")
        self.keywords_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_keywords_entry = ttk.Entry(entry_edit_frame, width=50)
        self.entry_keywords_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        ttk.Label(entry_edit_frame, text="(comma-separated)", font=('TkDefaultFont', 8, 'italic')).grid(
            row=2, column=2, sticky=tk.W, padx=5)
        
        # Entry action buttons
        entry_button_frame = ttk.Frame(entry_edit_frame)
        entry_button_frame.grid(row=3, column=1, pady=10)
        ttk.Button(entry_button_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Update Entry", command=self.update_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Clear Form", command=self.clear_entry_form).pack(side=tk.LEFT, padx=5)
        
        # Entries list
        entries_list_frame = ttk.LabelFrame(entry_mgmt_frame, text="Entries in Selected Lorebook", padding=10)
        entries_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for entries list
        entries_scrollbar = ttk.Scrollbar(entries_list_frame)
        entries_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.entries_listbox = tk.Listbox(entries_list_frame, height=10, yscrollcommand=entries_scrollbar.set)
        self.entries_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        entries_scrollbar.config(command=self.entries_listbox.yview)
        self.entries_listbox.bind('<<ListboxSelect>>', self.on_entry_select)
        
        # Entry management buttons
        entry_mgmt_button_frame = ttk.Frame(entries_list_frame)
        entry_mgmt_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(entry_mgmt_button_frame, text="Edit Selected", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_mgmt_button_frame, text="Delete Selected", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_mgmt_button_frame, text="Refresh", command=self.refresh_entries_list).pack(side=tk.LEFT, padx=5)
        
        # Initialize
        self.current_lorebook = None
        self.current_entry_index = None
        self.refresh_lorebooks_list()
        self.on_activation_type_change()
    
    def on_activation_type_change(self):
        """Handle activation type change - show/hide keywords field"""
        if self.entry_activation_type.get() == "constant":
            self.keywords_label.config(state='disabled')
            self.entry_keywords_entry.config(state='disabled')
        else:
            self.keywords_label.config(state='normal')
            self.entry_keywords_entry.config(state='normal')
    
    def add_lorebook(self):
        """Add a new lorebook"""
        name = self.lorebook_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a lorebook name")
            return
        
        # Check if lorebook already exists
        if self.config_manager.get_lorebook_by_name(name):
            messagebox.showerror("Error", f"Lorebook '{name}' already exists")
            return
        
        self.config_manager.add_lorebook(name, active=True)
        self.lorebook_name_entry.delete(0, tk.END)
        self.refresh_lorebooks_list()
        messagebox.showinfo("Success", f"Lorebook '{name}' created successfully!")
    
    def activate_lorebook(self):
        """Activate selected lorebook"""
        selection = self.lorebooks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a lorebook")
            return
        
        index = selection[0]
        lorebooks = self.config_manager.get_lorebooks()
        if index < len(lorebooks):
            name = lorebooks[index]['name']
            self.config_manager.toggle_lorebook_active(name, True)
            self.refresh_lorebooks_list()
            messagebox.showinfo("Success", f"Lorebook '{name}' activated")
    
    def deactivate_lorebook(self):
        """Deactivate selected lorebook"""
        selection = self.lorebooks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a lorebook")
            return
        
        index = selection[0]
        lorebooks = self.config_manager.get_lorebooks()
        if index < len(lorebooks):
            name = lorebooks[index]['name']
            self.config_manager.toggle_lorebook_active(name, False)
            self.refresh_lorebooks_list()
            messagebox.showinfo("Success", f"Lorebook '{name}' deactivated")
    
    def delete_lorebook(self):
        """Delete selected lorebook"""
        selection = self.lorebooks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a lorebook to delete")
            return
        
        index = selection[0]
        lorebooks = self.config_manager.get_lorebooks()
        if index < len(lorebooks):
            name = lorebooks[index]['name']
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete lorebook '{name}'?"):
                self.config_manager.delete_lorebook(index)
                self.current_lorebook = None
                self.refresh_lorebooks_list()
                self.refresh_entries_list()
                messagebox.showinfo("Success", f"Lorebook '{name}' deleted")
    
    def refresh_lorebooks_list(self):
        """Refresh the lorebooks list"""
        self.lorebooks_listbox.delete(0, tk.END)
        lorebooks = self.config_manager.get_lorebooks()
        for lb in lorebooks:
            name = lb.get("name", "Unknown")
            active = "✓" if lb.get("active", False) else "✗"
            entry_count = len(lb.get("entries", []))
            self.lorebooks_listbox.insert(tk.END, f"{active} {name} ({entry_count} entries)")
    
    def on_lorebook_select(self, event):
        """Handle lorebook selection"""
        selection = self.lorebooks_listbox.curselection()
        if selection:
            index = selection[0]
            lorebooks = self.config_manager.get_lorebooks()
            if index < len(lorebooks):
                self.current_lorebook = lorebooks[index]['name']
                self.selected_lorebook_label.config(text=f"Selected: {self.current_lorebook}")
                self.refresh_entries_list()
    
    def add_entry(self):
        """Add a new entry to the selected lorebook"""
        if not self.current_lorebook:
            messagebox.showwarning("Warning", "Please select a lorebook first")
            return
        
        content = self.entry_content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter entry content")
            return
        
        activation_type = self.entry_activation_type.get()
        keywords = []
        
        if activation_type == "normal":
            keywords_str = self.entry_keywords_entry.get().strip()
            if not keywords_str:
                messagebox.showwarning("Warning", "Please enter at least one keyword for normal entries")
                return
            keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
        
        success = self.config_manager.add_lorebook_entry(
            self.current_lorebook, content, activation_type, keywords
        )
        
        if success:
            self.clear_entry_form()
            self.refresh_entries_list()
            self.refresh_lorebooks_list()  # Update entry count
            messagebox.showinfo("Success", "Entry added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add entry")
    
    def update_entry(self):
        """Update the selected entry"""
        if not self.current_lorebook:
            messagebox.showwarning("Warning", "Please select a lorebook first")
            return
        
        if self.current_entry_index is None:
            messagebox.showwarning("Warning", "Please select an entry to update")
            return
        
        content = self.entry_content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter entry content")
            return
        
        activation_type = self.entry_activation_type.get()
        keywords = []
        
        if activation_type == "normal":
            keywords_str = self.entry_keywords_entry.get().strip()
            if not keywords_str:
                messagebox.showwarning("Warning", "Please enter at least one keyword for normal entries")
                return
            keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
        
        success = self.config_manager.update_lorebook_entry(
            self.current_lorebook, self.current_entry_index, content, activation_type, keywords
        )
        
        if success:
            self.clear_entry_form()
            self.refresh_entries_list()
            messagebox.showinfo("Success", "Entry updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update entry")
    
    def delete_entry(self):
        """Delete the selected entry"""
        if not self.current_lorebook:
            messagebox.showwarning("Warning", "Please select a lorebook first")
            return
        
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        index = selection[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?"):
            success = self.config_manager.delete_lorebook_entry(self.current_lorebook, index)
            if success:
                self.clear_entry_form()
                self.refresh_entries_list()
                self.refresh_lorebooks_list()  # Update entry count
                messagebox.showinfo("Success", "Entry deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete entry")
    
    def edit_entry(self):
        """Load selected entry into the form for editing"""
        if not self.current_lorebook:
            messagebox.showwarning("Warning", "Please select a lorebook first")
            return
        
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        index = selection[0]
        lorebook = self.config_manager.get_lorebook_by_name(self.current_lorebook)
        if lorebook and index < len(lorebook.get("entries", [])):
            entry = lorebook["entries"][index]
            
            # Load entry data into form
            self.entry_content_text.delete("1.0", tk.END)
            self.entry_content_text.insert("1.0", entry.get("content", ""))
            
            activation_type = entry.get("insertion_type", "normal")
            self.entry_activation_type.set(activation_type)
            self.on_activation_type_change()
            
            keywords = entry.get("keywords", [])
            self.entry_keywords_entry.delete(0, tk.END)
            if keywords:
                self.entry_keywords_entry.insert(0, ", ".join(keywords))
            
            self.current_entry_index = index
    
    def clear_entry_form(self):
        """Clear the entry form"""
        self.entry_content_text.delete("1.0", tk.END)
        self.entry_activation_type.set("normal")
        self.entry_keywords_entry.delete(0, tk.END)
        self.current_entry_index = None
        self.on_activation_type_change()
    
    def refresh_entries_list(self):
        """Refresh the entries list for the selected lorebook"""
        self.entries_listbox.delete(0, tk.END)
        
        if not self.current_lorebook:
            self.selected_lorebook_label.config(text="No lorebook selected")
            return
        
        lorebook = self.config_manager.get_lorebook_by_name(self.current_lorebook)
        if lorebook:
            entries = lorebook.get("entries", [])
            for i, entry in enumerate(entries):
                content = entry.get("content", "")
                content_preview = content[:50] + "..." if len(content) > 50 else content
                activation_type = entry.get("insertion_type", "normal")
                type_label = "C" if activation_type == "constant" else "N"
                
                keywords = entry.get("keywords", [])
                keywords_preview = ""
                if activation_type == "normal" and keywords:
                    keywords_preview = f" [{', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}]"
                
                self.entries_listbox.insert(tk.END, f"[{type_label}] {content_preview}{keywords_preview}")
    
    def on_entry_select(self, event):
        """Handle entry selection"""
        # This is just for visual feedback; actual editing happens via Edit button
        pass
    
    def create_console_tab(self):
        """Create console tab for viewing AI request/response logs"""
        
        # Console frame
        console_frame = ttk.LabelFrame(self.console_frame, text="AI Request/Response Console", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Console text area with scrollbar
        console_scroll = ttk.Scrollbar(console_frame)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            height=25,
            width=80,
            state='disabled',
            yscrollcommand=console_scroll.set,
            wrap=tk.WORD
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        console_scroll.config(command=self.console_text.yview)
        
        # Configure text tags for different log types
        self.console_text.tag_config('header', foreground='blue', font=('TkDefaultFont', 10, 'bold'))
        self.console_text.tag_config('request', foreground='green')
        self.console_text.tag_config('response', foreground='purple')
        self.console_text.tag_config('error', foreground='red')
        self.console_text.tag_config('info', foreground='gray')
        self.console_text.tag_config('timestamp', foreground='navy', font=('TkDefaultFont', 8))
        
        # Control buttons
        button_frame = ttk.Frame(console_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(button_frame, text="Auto-scroll", variable=self.auto_scroll_var).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Log", command=self.export_console_log).pack(side=tk.LEFT, padx=5)
        
        # Initialize console with welcome message
        self.log_to_console("Console initialized. AI requests and responses will appear here.", 'info')
    
    def log_to_console(self, message, tag='info'):
        """Log a message to the console"""
        import datetime
        
        self.console_text.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add message
        self.console_text.insert(tk.END, f"{message}\n", tag)
        
        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.console_text.see(tk.END)
        
        self.console_text.config(state='disabled')
    
    def clear_console(self):
        """Clear the console"""
        self.console_text.config(state='normal')
        self.console_text.delete("1.0", tk.END)
        self.console_text.config(state='disabled')
        self.log_to_console("Console cleared.", 'info')
    
    def export_console_log(self):
        """Export console log to a file"""
        filename = filedialog.asksaveasfilename(
            title="Export Console Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.console_text.get("1.0", tk.END))
                messagebox.showinfo("Success", f"Console log exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export log: {str(e)}")
    
    def on_closing(self):
        """Handle window close event gracefully"""
        try:
            # Stop any running Discord client
            if self.discord_client and not self.discord_client.is_closed():
                self.discord_client.close()
        except Exception as e:
            print(f"Error closing Discord client: {str(e)}")
        finally:
            self.root.destroy()


def main():
    """Main entry point for GUI"""
    try:
        root = tk.Tk()
        app = PresetBotGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print(f"Fatal error in GUI: {str(e)}")
        print(traceback.format_exc())
        try:
            messagebox.showerror("Fatal Error", f"The application encountered a fatal error:\n{str(e)}\n\nCheck console for details.")
        except:
            pass


if __name__ == "__main__":
    main()
