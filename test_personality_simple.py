#!/usr/bin/env python3
"""
Simple test to verify the personality assistant functionality works.
"""

from ai_agent import generate_system_prompt

def test_personality_prompts():
    """Test that different personalities generate different prompts"""
    print("Testing personality prompt generation...")
    
    # Test predefined personalities with expected keywords
    personality_keywords = {
        "doctor": "medical",
        "lawyer": "legal", 
        "receptionist": "receptionist",
        "teacher": "educational",
        "therapist": "therapeutic",
        "hr": "hr"
    }
    
    for personality, expected_keyword in personality_keywords.items():
        prompt = generate_system_prompt(personality)
        print(f"\n--- {personality.upper()} PERSONALITY ---")
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
        
        # Basic assertion that the expected keyword is mentioned in the prompt
        if personality == "hr":
            assert "hr" in prompt.lower() or "interview" in prompt.lower(), f"Expected HR-related keyword not found in {personality} prompt"
        else:
            assert expected_keyword.lower() in prompt.lower(), f"Expected keyword '{expected_keyword}' not found in {personality} prompt"
    
    # Test custom personality
    custom_personality = "software engineer"
    custom_prompt = generate_system_prompt(custom_personality)
    print(f"\n--- CUSTOM PERSONALITY: {custom_personality.upper()} ---")
    print(custom_prompt[:200] + "..." if len(custom_prompt) > 200 else custom_prompt)
    
    assert custom_personality.lower() in custom_prompt.lower(), f"Custom personality '{custom_personality}' not found in prompt"
    
    print("\n✅ All personality prompt tests passed!")

if __name__ == "__main__":
    print("🧪 Running Personality Assistant Tests")
    print("=" * 50)
    
    try:
        test_personality_prompts()
        
        print("\n🎉 All tests passed!")
        print("The personality assistant prompt generation is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import sys
        sys.exit(1)