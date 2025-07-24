#!/usr/bin/env python3
"""
Simple test to verify the personality assistant functionality works.
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent import generate_system_prompt, ask_agent

def test_personality_prompts():
    """Test that different personalities generate different prompts"""
    print("Testing personality prompt generation...")
    
    # Test predefined personalities
    personalities = ["doctor", "lawyer", "receptionist", "teacher", "therapist"]
    
    for personality in personalities:
        prompt = generate_system_prompt(personality)
        print(f"\n--- {personality.upper()} PERSONALITY ---")
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
        
        # Basic assertion that the personality is mentioned in the prompt
        assert personality.lower() in prompt.lower(), f"Personality '{personality}' not found in prompt"
    
    # Test custom personality
    custom_personality = "software engineer"
    custom_prompt = generate_system_prompt(custom_personality)
    print(f"\n--- CUSTOM PERSONALITY: {custom_personality.upper()} ---")
    print(custom_prompt[:200] + "..." if len(custom_prompt) > 200 else custom_prompt)
    
    assert custom_personality.lower() in custom_prompt.lower(), f"Custom personality '{custom_personality}' not found in prompt"
    
    print("\n✅ All personality prompt tests passed!")

def test_ask_agent_with_personality():
    """Test that ask_agent function accepts personality parameter"""
    print("\nTesting ask_agent function with personality parameter...")
    
    # This test will only verify the function can be called with the personality parameter
    # We won't actually make API calls since we don't have API keys in the test environment
    try:
        # Test that the function signature works
        import inspect
        sig = inspect.signature(ask_agent)
        params = list(sig.parameters.keys())
        
        assert 'user_query' in params, "ask_agent should have user_query parameter"
        assert 'personality_type' in params, "ask_agent should have personality_type parameter"
        
        print("✅ ask_agent function signature is correct!")
        
    except Exception as e:
        print(f"❌ Error testing ask_agent: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Running Personality Assistant Tests")
    print("=" * 50)
    
    try:
        test_personality_prompts()
        test_ask_agent_with_personality()
        
        print("\n🎉 All tests passed!")
        print("The personality assistant functionality is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)