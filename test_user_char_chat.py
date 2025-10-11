#!/usr/bin/env python3
"""
Test that user character description is passed to AI correctly
"""

import sys
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# We need to test the actual bot.py logic
from bot import AIResponseHandler, ConfigManager

def test_user_character_info_in_system_prompt():
    """Test that user character info is added to system prompt"""
    
    # Create mock config manager
    config_manager = MagicMock(spec=ConfigManager)
    config_manager.get_character_by_name.return_value = {
        "name": "assistant",
        "description": "You are a helpful assistant."
    }
    config_manager.get_active_lorebook_entries.return_value = []
    config_manager.get_active_preset.return_value = None
    config_manager.get_selected_model.return_value = "gpt-3.5-turbo"
    config_manager.get_openai_config.return_value = {
        "base_url": "https://api.openai.com/v1",
        "api_key": "test-key"
    }
    
    # Create AI handler
    ai_handler = AIResponseHandler(config_manager)
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    
    async def mock_create(*args, **kwargs):
        # Capture the messages sent to OpenAI
        messages = kwargs.get('messages', [])
        
        # Find system message
        system_messages = [msg for msg in messages if msg.get('role') == 'system']
        
        if system_messages:
            system_content = system_messages[0]['content']
            print(f"System prompt: {system_content}")
            
            # Check that user character info is in the system prompt
            assert "Alice" in system_content, "User character name should be in system prompt"
            assert "brave warrior" in system_content, "User character description should be in system prompt"
        else:
            raise AssertionError("No system message found in messages!")
        
        return mock_response
    
    mock_client.chat.completions.create = AsyncMock(side_effect=mock_create)
    ai_handler.client = mock_client
    
    # Test with user character info
    user_char_info = "\n\nUser is playing as Alice.\nCharacter description: Alice is a brave warrior."
    
    async def run_test():
        response = await ai_handler.get_ai_response(
            "Hello!",
            character_name="assistant",
            user_character_info=user_char_info
        )
        print(f"✓ Test passed! User character info was added to system prompt")
        return response
    
    # Run the async test
    asyncio.run(run_test())

if __name__ == "__main__":
    print("Testing user character info in system prompt...")
    test_user_character_info_in_system_prompt()
    print("✓ All tests passed!")
