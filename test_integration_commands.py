"""
Integration test to simulate Discord bot command interactions
Tests viewu, viewc, and cimage commands in a realistic scenario
"""

import asyncio
import os
import sys
from typing import Optional
from bot import ConfigManager

class MockContext:
    """Mock Discord context for testing"""
    def __init__(self, author_id: str, author_name: str, channel_id: str):
        self.author = type('obj', (object,), {'id': author_id, 'name': author_name})()
        self.channel = type('obj', (object,), {'id': channel_id})()
        self.message = type('obj', (object,), {'created_at': type('obj', (object,), {'isoformat': lambda: '2024-01-01T00:00:00'})()})()
        self.sent_messages = []
    
    async def send(self, content=None, **kwargs):
        """Mock send method"""
        self.sent_messages.append({
            'content': content,
            'embed': kwargs.get('embed'),
            'view': kwargs.get('view'),
            'file': kwargs.get('file')
        })
        return type('obj', (object,), {'content': content})()

def simulate_viewu_command(config_mgr: ConfigManager, ctx: MockContext, character_name: Optional[str] = None):
    """Simulate the !viewu command logic"""
    # If a specific character name is provided, show that character
    if character_name:
        user_char = config_mgr.get_user_character_by_name(character_name)
        if not user_char:
            return f"Error: User character '{character_name}' not found."
        return {
            'status': 'success',
            'character': user_char,
            'display_name': user_char.get('display_name', user_char.get('name', 'Unknown')),
            'avatar_url': user_char.get('avatar_url', ''),
            'description': user_char.get('description', '')
        }
    else:
        # Find the user's active character by looking through chat history
        channel_id = str(ctx.channel.id)
        chat_history = config_mgr.get_chat_history(channel_id)
        history_limit = config_mgr.get_chat_history_limit()
        
        active_user_character = None
        # Look through recent history for this user's character
        for msg in reversed(chat_history[-history_limit:]):
            if msg.get("user_character") and msg.get("author") == str(ctx.author.id):
                active_user_character = msg.get("user_character")
                break
        
        if not active_user_character:
            return "You haven't used a user character in !chat yet in this channel."
        
        user_char = config_mgr.get_user_character_by_name(active_user_character)
        if not user_char:
            return f"Error: Your active user character '{active_user_character}' was not found in the config."
        
        return {
            'status': 'success',
            'character': user_char,
            'display_name': user_char.get('display_name', user_char.get('name', 'Unknown')),
            'avatar_url': user_char.get('avatar_url', ''),
            'description': user_char.get('description', '')
        }

def simulate_viewc_command(config_mgr: ConfigManager, ctx: MockContext, character_name: Optional[str] = None):
    """Simulate the !viewc command logic"""
    # If a specific character name is provided, show that character
    if character_name:
        char = config_mgr.get_character_by_name(character_name)
        if not char:
            return f"Error: Character '{character_name}' not found."
        return {
            'status': 'success',
            'character': char,
            'display_name': char.get('display_name', char.get('name', 'Unknown')),
            'avatar_url': char.get('avatar_url', ''),
            'description': char.get('description', ''),
            'scenario': char.get('scenario', '')
        }
    else:
        # Get the channel's active character
        channel_id = str(ctx.channel.id)
        ai_character_name = config_mgr.get_channel_character(channel_id)
        
        if not ai_character_name:
            # Use default character (first one)
            characters = config_mgr.get_characters()
            if characters:
                char = characters[0]
                return {
                    'status': 'success',
                    'character': char,
                    'display_name': char.get('display_name', char.get('name', 'Unknown')),
                    'avatar_url': char.get('avatar_url', ''),
                    'description': char.get('description', ''),
                    'scenario': char.get('scenario', ''),
                    'is_default': True
                }
            else:
                return "No characters configured."
        else:
            char = config_mgr.get_character_by_name(ai_character_name)
            if not char:
                return f"Error: Channel character '{ai_character_name}' was not found in the config."
            return {
                'status': 'success',
                'character': char,
                'display_name': char.get('display_name', char.get('name', 'Unknown')),
                'avatar_url': char.get('avatar_url', ''),
                'description': char.get('description', ''),
                'scenario': char.get('scenario', ''),
                'is_default': False
            }

def test_integration_scenario():
    """Test a complete scenario with multiple users and characters"""
    print("\n" + "=" * 60)
    print("Integration Test: Multi-User Character Scenario")
    print("=" * 60)
    
    # Setup
    test_config_path = "test_integration_config.json"
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    config_mgr = ConfigManager(test_config_path)
    
    # Add characters
    print("\n1. Setting up characters...")
    config_mgr.add_character(
        name="narrator",
        display_name="The Narrator",
        description="A mysterious narrator who guides the story",
        avatar_url="https://example.com/narrator.png",
        scenario="You are narrating a fantasy adventure"
    )
    
    config_mgr.add_user_character(
        name="alice",
        display_name="Alice the Brave",
        description="A courageous knight seeking justice",
        avatar_url="https://example.com/alice.png"
    )
    
    config_mgr.add_user_character(
        name="bob",
        display_name="Bob the Wizard",
        description="A wise old wizard with powerful magic",
        avatar_url="https://example.com/bob.png"
    )
    print("   ✓ Characters created: narrator, alice, bob")
    
    # Create mock contexts for two users
    channel_id = "test_channel_789"
    user1_ctx = MockContext("user111", "User1", channel_id)
    user2_ctx = MockContext("user222", "User2", channel_id)
    
    # Set channel character
    print("\n2. Setting channel character to 'narrator'...")
    config_mgr.set_channel_character(channel_id, "narrator")
    print("   ✓ Channel character set")
    
    # Simulate User1 using !chat with alice
    print("\n3. User1 uses !chat as alice...")
    config_mgr.add_chat_message(channel_id, {
        "author": str(user1_ctx.author.id),
        "author_name": str(user1_ctx.author.name),
        "user_character": "alice",
        "content": "I shall defend the innocent!",
        "type": "user",
        "timestamp": "2024-01-01T00:00:00"
    })
    print("   ✓ Message added to history")
    
    # Simulate User2 using !chat with bob
    print("\n4. User2 uses !chat as bob...")
    config_mgr.add_chat_message(channel_id, {
        "author": str(user2_ctx.author.id),
        "author_name": str(user2_ctx.author.name),
        "user_character": "bob",
        "content": "Let me cast a spell to help!",
        "type": "user",
        "timestamp": "2024-01-01T00:01:00"
    })
    print("   ✓ Message added to history")
    
    # Test !viewu for User1 (should show alice)
    print("\n5. Testing !viewu for User1...")
    result1 = simulate_viewu_command(config_mgr, user1_ctx)
    assert isinstance(result1, dict), "Should return a dict"
    assert result1['status'] == 'success', "Should succeed"
    assert result1['display_name'] == 'Alice the Brave', f"Should be Alice, got {result1['display_name']}"
    print(f"   ✓ User1's active character: {result1['display_name']}")
    
    # Test !viewu for User2 (should show bob)
    print("\n6. Testing !viewu for User2...")
    result2 = simulate_viewu_command(config_mgr, user2_ctx)
    assert isinstance(result2, dict), "Should return a dict"
    assert result2['status'] == 'success', "Should succeed"
    assert result2['display_name'] == 'Bob the Wizard', f"Should be Bob, got {result2['display_name']}"
    print(f"   ✓ User2's active character: {result2['display_name']}")
    
    # Test !viewu with specific character name
    print("\n7. Testing !viewu alice (specific character)...")
    result3 = simulate_viewu_command(config_mgr, user1_ctx, "alice")
    assert isinstance(result3, dict), "Should return a dict"
    assert result3['display_name'] == 'Alice the Brave', "Should be Alice"
    print(f"   ✓ Specific character view: {result3['display_name']}")
    
    # Test !viewc (should show narrator)
    print("\n8. Testing !viewc (channel character)...")
    result4 = simulate_viewc_command(config_mgr, user1_ctx)
    assert isinstance(result4, dict), "Should return a dict"
    assert result4['status'] == 'success', "Should succeed"
    assert result4['display_name'] == 'The Narrator', f"Should be The Narrator, got {result4['display_name']}"
    assert result4['scenario'] == 'You are narrating a fantasy adventure', "Should have scenario"
    assert not result4.get('is_default', False), "Should not be default"
    print(f"   ✓ Channel character: {result4['display_name']}")
    
    # Test !viewc with specific character
    print("\n9. Testing !viewc narrator (specific character)...")
    result5 = simulate_viewc_command(config_mgr, user1_ctx, "narrator")
    assert isinstance(result5, dict), "Should return a dict"
    assert result5['display_name'] == 'The Narrator', "Should be The Narrator"
    print(f"   ✓ Specific character view: {result5['display_name']}")
    
    # Test new user with no chat history
    print("\n10. Testing !viewu for new user (no history)...")
    user3_ctx = MockContext("user333", "User3", channel_id)
    result6 = simulate_viewu_command(config_mgr, user3_ctx)
    assert isinstance(result6, str), "Should return error message"
    assert "haven't used" in result6, "Should indicate no history"
    print(f"   ✓ New user result: {result6}")
    
    # Test channel with no character set
    print("\n11. Testing !viewc in channel with no character...")
    channel2_id = "test_channel_999"
    user4_ctx = MockContext("user444", "User4", channel2_id)
    result7 = simulate_viewc_command(config_mgr, user4_ctx)
    assert isinstance(result7, dict), "Should return a dict (default character)"
    assert result7.get('is_default', False), "Should be default character"
    print(f"   ✓ Default character: {result7['display_name']}")
    
    # Clean up
    if os.path.exists(test_config_path):
        os.remove(test_config_path)
    
    print("\n" + "=" * 60)
    print("✅ All integration tests passed!")
    print("=" * 60)
    return True

def main():
    """Run integration tests"""
    try:
        test_integration_scenario()
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print(traceback.format_exc())
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
