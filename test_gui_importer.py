#!/usr/bin/env python3
"""
Quick test of the lorebook importer GUI
"""

import tkinter as tk
from gui import PresetBotGUI

def main():
    print("Starting GUI test...")
    print("Navigate to the Lorebooks tab and click 'Import...' to test the importer")
    print("Sample files available:")
    print("  - sample_lorebook.json (single lorebook)")
    print("  - sample_config_format.json (config with multiple lorebooks)")
    
    root = tk.Tk()
    app = PresetBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
