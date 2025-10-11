"""
Test config reload functionality
"""
import os
import json
from bot import ConfigManager


def test_config_reload():
    """Test that config reload picks up external changes"""
    
    # Create a test config file
    test_config = "test_reload_config.json"
    
    # Clean up if exists
    if os.path.exists(test_config):
        os.remove(test_config)
    
    try:
        # Initialize config manager with test config
        config_mgr = ConfigManager(test_config)
        
        # Add a character
        config_mgr.add_character("test_char", "Test Character", "A test character")
        
        # Verify it's there
        chars = config_mgr.get_characters()
        assert len(chars) == 2  # Default assistant + test_char
        print("✓ Character added to config")
        
        # Simulate external change: modify the config file directly
        with open(test_config, 'r') as f:
            config_data = json.load(f)
        
        # Add another character directly to the file
        config_data['characters'].append({
            "name": "external_char",
            "display_name": "External Character",
            "description": "Added externally",
            "scenario": "",
            "avatar_url": "",
            "avatar_file": ""
        })
        
        with open(test_config, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print("✓ External character added to config file")
        
        # Without reload, the config manager shouldn't see it
        chars = config_mgr.get_characters()
        assert len(chars) == 2, "Should still be 2 characters before reload"
        print("✓ Config manager doesn't see external changes yet")
        
        # Now reload
        config_mgr.reload_config()
        
        # After reload, should see the external character
        chars = config_mgr.get_characters()
        assert len(chars) == 3, f"Should be 3 characters after reload, got {len(chars)}"
        
        # Verify the external character is there
        char_names = [c['name'] for c in chars]
        assert 'external_char' in char_names, "External character should be present"
        
        print("✓ Config reload successfully picked up external changes")
        
        # Test that lorebook changes are also picked up
        config_mgr.add_lorebook("test_lorebook", active=True)
        
        # Modify lorebook externally
        with open(test_config, 'r') as f:
            config_data = json.load(f)
        
        config_data['lorebooks'][0]['active'] = False
        
        with open(test_config, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        # Before reload
        lorebooks = config_mgr.get_lorebooks()
        assert lorebooks[0]['active'] == True, "Should still be active before reload"
        
        # After reload
        config_mgr.reload_config()
        lorebooks = config_mgr.get_lorebooks()
        assert lorebooks[0]['active'] == False, "Should be inactive after reload"
        
        print("✓ Lorebook changes also picked up by reload")
        
        print("\n✅ Config reload test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_config):
            os.remove(test_config)


if __name__ == "__main__":
    print("Testing config reload functionality...\n")
    test_config_reload()
