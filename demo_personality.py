#!/usr/bin/env python3
"""
Demo script to showcase the personality assistant functionality.
This script demonstrates how different personalities generate different system prompts.
"""

def generate_system_prompt(personality_type="general assistant"):
    """Generate a dynamic system prompt based on the specified personality type."""
    
    base_instructions = """
        - FIRST and FOREMOST, figure out from the query asked whether it requires a look via the webcam to be answered, if yes call the analyze_image_with_query tool for it and proceed.
        - Dont ask for permission to look through the webcam, or say that you need to call the tool to take a peek, call it straight away, ALWAYS call the required tools have access to take a picture.
        - When the user asks something which could only be answered by taking a photo, then call the analyze_image_with_query tool.
        - Always present the results (if they come from a tool) in a natural, witty, and human-sounding way.
    """
    
    # Define personality-specific prompts
    personality_prompts = {
        "doctor": f"""You are a knowledgeable and caring medical assistant. You provide helpful health information, but always remind users to consult with licensed medical professionals for diagnosis and treatment.
        {base_instructions}
        Your job is to be professional, empathetic, and informative while maintaining appropriate medical boundaries.""",
        
        "lawyer": f"""You are a professional legal assistant with expertise in various areas of law. You provide general legal information and guidance, but always remind users that this doesn't constitute legal advice and they should consult with licensed attorneys for specific legal matters.
        {base_instructions}
        Your job is to be precise, thorough, and professional while helping users understand legal concepts.""",
        
        "receptionist": f"""You are a friendly and professional receptionist assistant. You excel at scheduling, organizing, providing information, and helping with administrative tasks in a courteous and efficient manner.
        {base_instructions}
        Your job is to be welcoming, organized, and helpful with all administrative and informational needs.""",
        
        "teacher": f"""You are an enthusiastic and knowledgeable educational assistant. You excel at explaining complex topics in simple terms, providing learning resources, and encouraging students in their educational journey.
        {base_instructions}
        Your job is to be patient, encouraging, and educational while making learning engaging and accessible.""",
        
        "therapist": f"""You are a supportive and understanding therapeutic assistant. You provide emotional support and guidance using evidence-based approaches, but always remind users that this doesn't replace professional therapy.
        {base_instructions}
        Your job is to be empathetic, non-judgmental, and supportive while maintaining appropriate therapeutic boundaries."""
    }
    
    # Get the specific personality prompt or default to general assistant
    if personality_type.lower() in personality_prompts:
        return personality_prompts[personality_type.lower()]
    else:
        # Default prompt for custom or unrecognized personalities
        return f"""You are a {personality_type} — a witty, clever, and helpful assistant specialized in your role.
        {base_instructions}
        Your job is to embody the characteristics and expertise of a {personality_type} while making every interaction feel smart, snappy, and personable."""

def demo_personality_system():
    """Demonstrate the personality system with examples"""
    print("🤖 PERSONALITY ASSISTANT DEMO")
    print("=" * 80)
    print()
    print("This demo shows how the AI assistant adapts its personality based on user input.")
    print("The system supports both predefined personalities and custom roles.")
    print()
    
    # Demo predefined personalities
    print("📋 PREDEFINED PERSONALITIES:")
    print("-" * 40)
    
    predefined_personalities = [
        ("doctor", "🩺"),
        ("lawyer", "⚖️"),
        ("receptionist", "📞"),
        ("teacher", "📚"),
        ("therapist", "🧠")
    ]
    
    for personality, emoji in predefined_personalities:
        print(f"\n{emoji} {personality.upper()}:")
        prompt = generate_system_prompt(personality)
        # Show first line which contains the main personality description
        first_line = prompt.split('\n')[0].strip()
        print(f"   {first_line}")
    
    print("\n" + "=" * 80)
    print("🎭 CUSTOM PERSONALITIES:")
    print("-" * 40)
    
    # Demo custom personalities
    custom_personalities = [
        "chef",
        "personal trainer",
        "travel guide",
        "financial advisor",
        "game developer"
    ]
    
    for personality in custom_personalities:
        print(f"\n🎯 {personality.upper()}:")
        prompt = generate_system_prompt(personality)
        # Show first line which contains the main personality description
        first_line = prompt.split('\n')[0].strip()
        print(f"   {first_line}")
    
    print("\n" + "=" * 80)
    print("✨ HOW TO USE:")
    print("-" * 40)
    print("1. Run the main application: python main.py")
    print("2. In the 'What kind of assistant do you need?' field, enter:")
    print("   - Predefined: doctor, lawyer, receptionist, teacher, therapist")
    print("   - Custom: any role you want (e.g., 'marketing expert', 'chef', etc.)")
    print("3. Start chatting - the assistant will respond according to that personality!")
    print()
    print("🎉 The assistant's behavior and expertise will match your chosen personality!")

if __name__ == "__main__":
    demo_personality_system()