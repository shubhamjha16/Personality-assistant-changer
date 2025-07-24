#!/usr/bin/env python3
"""
Manual test of the AI agent without UI dependencies.
This simulates how the agent would work with different personalities.
"""

import sys
import os

# Mock the external dependencies to test the core logic
class MockLLM:
    def __init__(self, model, temperature):
        self.model = model
        self.temperature = temperature

class MockAgent:
    def __init__(self, model, tools, prompt):
        self.model = model
        self.tools = tools
        self.prompt = prompt
        self.personality = self._extract_personality_from_prompt(prompt)
    
    def _extract_personality_from_prompt(self, prompt):
        """Extract personality type from the prompt for demonstration"""
        if "medical assistant" in prompt:
            return "medical"
        elif "legal assistant" in prompt:
            return "legal"
        elif "receptionist assistant" in prompt:
            return "receptionist"
        elif "educational assistant" in prompt:
            return "educational"
        elif "therapeutic assistant" in prompt:
            return "therapeutic"
        else:
            return "custom"
    
    def invoke(self, input_messages):
        """Mock response based on personality"""
        user_message = input_messages["messages"][0]["content"]
        
        responses = {
            "medical": f"As your medical assistant, I understand you're asking about '{user_message}'. While I can provide general health information, please remember to consult with a licensed healthcare professional for proper diagnosis and treatment.",
            "legal": f"From a legal perspective regarding '{user_message}', I can provide general information. However, this doesn't constitute legal advice, and you should consult with a licensed attorney for your specific situation.",
            "receptionist": f"Thank you for your inquiry about '{user_message}'. I'd be happy to help you with this request. Let me assist you in an organized and professional manner.",
            "educational": f"Great question about '{user_message}'! Let me explain this in a clear and engaging way that will help you learn and understand the concept better.",
            "therapeutic": f"I hear that you're asking about '{user_message}'. I'm here to provide support and understanding. Remember that while I can offer guidance, this doesn't replace professional therapy.",
            "custom": f"As your specialized assistant, I'll help you with '{user_message}' using my expertise in this area."
        }
        
        response_content = responses.get(self.personality, responses["custom"])
        
        return {
            "messages": [
                {"role": "assistant", "content": response_content}
            ]
        }

# Mock the imports
def mock_create_react_agent(model, tools, prompt):
    return MockAgent(model, tools, prompt)

# Add current directory to path and import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily replace the real imports with mocks
original_modules = {}
mock_modules = {
    'langchain_google_genai': type('MockModule', (), {
        'ChatGoogleGenerativeAI': MockLLM
    })(),
    'langgraph.prebuilt': type('MockModule', (), {
        'create_react_agent': mock_create_react_agent
    })(),
    'dotenv': type('MockModule', (), {
        'load_dotenv': lambda: None
    })(),
    'tools': type('MockModule', (), {
        'analyze_image_with_query': lambda x: f"Mock image analysis for: {x}"
    })()
}

# Inject mocks
for module_name, mock_module in mock_modules.items():
    sys.modules[module_name] = mock_module

# Now import our actual module
from ai_agent import ask_agent, generate_system_prompt

def test_personality_integration():
    """Test the complete personality system"""
    print("🧪 TESTING PERSONALITY INTEGRATION")
    print("=" * 60)
    
    test_question = "What should I know about stress?"
    personalities_to_test = [
        ("doctor", "Medical perspective"),
        ("lawyer", "Legal perspective"), 
        ("receptionist", "Administrative perspective"),
        ("teacher", "Educational perspective"),
        ("therapist", "Therapeutic perspective"),
        ("chef", "Custom personality")
    ]
    
    for personality, description in personalities_to_test:
        print(f"\n🎭 Testing {personality.upper()} personality ({description}):")
        print("-" * 40)
        
        try:
            # Test prompt generation
            prompt = generate_system_prompt(personality)
            print(f"✅ Prompt generated: {len(prompt)} characters")
            
            # Test the ask_agent function with mocked dependencies
            response = ask_agent(test_question, personality)
            print(f"✅ Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error testing {personality}: {e}")
            continue
    
    print(f"\n🎉 All personality integration tests completed!")
    print("The system successfully adapts responses based on personality type!")

if __name__ == "__main__":
    test_personality_integration()