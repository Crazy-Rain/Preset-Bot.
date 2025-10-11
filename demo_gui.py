#!/usr/bin/env python3
"""
Simple script to demonstrate the new GUI tabs without requiring a full setup
This creates a mock GUI to show the layout
"""

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    
    def create_demo_gui():
        """Create a demo GUI showing the new tabs"""
        root = tk.Tk()
        root.title("Preset Discord Bot - GUI Demo (New Features)")
        root.geometry("900x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lorebooks Tab Demo
        lorebooks_frame = ttk.Frame(notebook)
        notebook.add(lorebooks_frame, text="Lorebooks")
        
        # Main container with horizontal split
        main_paned = ttk.PanedWindow(lorebooks_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Lorebook list
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        lorebook_mgmt_frame = ttk.LabelFrame(left_frame, text="Lorebook Management", padding=10)
        lorebook_mgmt_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add lorebook section
        add_lb_frame = ttk.Frame(lorebook_mgmt_frame)
        add_lb_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_lb_frame, text="New Lorebook:").pack(side=tk.LEFT, padx=5)
        lorebook_name_entry = ttk.Entry(add_lb_frame, width=20)
        lorebook_name_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(add_lb_frame, text="Create").pack(side=tk.LEFT, padx=5)
        
        # Lorebook list
        list_frame = ttk.Frame(lorebook_mgmt_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lorebooks_listbox = tk.Listbox(list_frame, height=10, yscrollcommand=scrollbar.set)
        lorebooks_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=lorebooks_listbox.yview)
        
        # Add demo items
        lorebooks_listbox.insert(tk.END, "✓ fantasy_world (3 entries)")
        lorebooks_listbox.insert(tk.END, "✗ sci_fi_universe (1 entries)")
        
        # Lorebook action buttons
        lb_button_frame = ttk.Frame(lorebook_mgmt_frame)
        lb_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(lb_button_frame, text="Activate").pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Deactivate").pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Delete").pack(side=tk.LEFT, padx=5)
        ttk.Button(lb_button_frame, text="Refresh").pack(side=tk.LEFT, padx=5)
        
        # Right panel - Entry management
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        entry_mgmt_frame = ttk.LabelFrame(right_frame, text="Entry Management", padding=10)
        entry_mgmt_frame.pack(fill=tk.BOTH, expand=True)
        
        # Selected lorebook label
        selected_lorebook_label = ttk.Label(entry_mgmt_frame, text="Selected: fantasy_world", 
                                             font=('TkDefaultFont', 10, 'bold'))
        selected_lorebook_label.pack(pady=5)
        
        # Add/Edit Entry section
        entry_edit_frame = ttk.LabelFrame(entry_mgmt_frame, text="Add/Edit Entry", padding=10)
        entry_edit_frame.pack(fill=tk.X, pady=5)
        
        # Entry content
        ttk.Label(entry_edit_frame, text="Content:").grid(row=0, column=0, sticky=tk.NW, pady=5)
        entry_content_text = scrolledtext.ScrolledText(entry_edit_frame, height=4, width=50)
        entry_content_text.grid(row=0, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        entry_content_text.insert("1.0", "This is a high-fantasy medieval world.")
        
        # Activation type
        ttk.Label(entry_edit_frame, text="Activation Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_activation_type = tk.StringVar(value="constant")
        type_frame = ttk.Frame(entry_edit_frame)
        type_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(type_frame, text="Constant (Always Active)", variable=entry_activation_type, 
                       value="constant").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Normal (Keyword Triggered)", variable=entry_activation_type, 
                       value="normal").pack(anchor=tk.W)
        
        # Keywords
        ttk.Label(entry_edit_frame, text="Keywords:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_keywords_entry = ttk.Entry(entry_edit_frame, width=50)
        entry_keywords_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        entry_keywords_entry.insert(0, "dragon, dragons, wyrm")
        ttk.Label(entry_edit_frame, text="(comma-separated)", font=('TkDefaultFont', 8, 'italic')).grid(
            row=2, column=2, sticky=tk.W, padx=5)
        
        # Entry action buttons
        entry_button_frame = ttk.Frame(entry_edit_frame)
        entry_button_frame.grid(row=3, column=1, pady=10)
        ttk.Button(entry_button_frame, text="Add Entry").pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Update Entry").pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_button_frame, text="Clear Form").pack(side=tk.LEFT, padx=5)
        
        # Entries list
        entries_list_frame = ttk.LabelFrame(entry_mgmt_frame, text="Entries in Selected Lorebook", padding=10)
        entries_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for entries list
        entries_scrollbar = ttk.Scrollbar(entries_list_frame)
        entries_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        entries_listbox = tk.Listbox(entries_list_frame, height=10, yscrollcommand=entries_scrollbar.set)
        entries_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        entries_scrollbar.config(command=entries_listbox.yview)
        
        # Add demo entries
        entries_listbox.insert(tk.END, "[C] This is a high-fantasy medieval world.")
        entries_listbox.insert(tk.END, "[N] Dragons are wise, ancient beings. [dragon, dragons]")
        entries_listbox.insert(tk.END, "[N] Elves live in forest cities. [elf, elves]")
        
        # Entry management buttons
        entry_mgmt_button_frame = ttk.Frame(entries_list_frame)
        entry_mgmt_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(entry_mgmt_button_frame, text="Edit Selected").pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_mgmt_button_frame, text="Delete Selected").pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_mgmt_button_frame, text="Refresh").pack(side=tk.LEFT, padx=5)
        
        # Console Tab Demo
        console_frame = ttk.Frame(notebook)
        notebook.add(console_frame, text="Console")
        
        console_lf = ttk.LabelFrame(console_frame, text="AI Request/Response Console", padding=10)
        console_lf.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Console text area
        console_scroll = ttk.Scrollbar(console_lf)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        console_text = scrolledtext.ScrolledText(
            console_lf,
            height=25,
            width=80,
            yscrollcommand=console_scroll.set,
            wrap=tk.WORD
        )
        console_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        console_scroll.config(command=console_text.yview)
        
        # Configure text tags
        console_text.tag_config('header', foreground='blue', font=('TkDefaultFont', 10, 'bold'))
        console_text.tag_config('request', foreground='green')
        console_text.tag_config('response', foreground='purple')
        console_text.tag_config('error', foreground='red')
        console_text.tag_config('info', foreground='gray')
        console_text.tag_config('timestamp', foreground='navy', font=('TkDefaultFont', 8))
        
        # Add demo content
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        console_text.insert(tk.END, "Console initialized. AI requests and responses will appear here.\n", 'info')
        
        console_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        console_text.insert(tk.END, "Testing OpenAI connection...\n", 'info')
        
        console_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        console_text.insert(tk.END, "Sending test request to https://api.openai.com/v1\n", 'request')
        
        console_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        console_text.insert(tk.END, "Response received: Connection successful!\n", 'response')
        
        # Control buttons
        button_frame = ttk.Frame(console_lf)
        button_frame.pack(fill=tk.X, pady=5)
        
        auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(button_frame, text="Auto-scroll", variable=auto_scroll_var).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Console").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Log").pack(side=tk.LEFT, padx=5)
        
        root.mainloop()
    
    if __name__ == "__main__":
        create_demo_gui()
        
except ImportError:
    print("This demo requires tkinter to be installed.")
    print("On Ubuntu/Debian: sudo apt-get install python3-tk")
    print("The actual GUI implementation is complete in gui.py")
