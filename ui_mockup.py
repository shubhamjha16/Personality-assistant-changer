#!/usr/bin/env python3
"""
Simple UI mockup to show what the personality assistant interface looks like
"""

import gradio as gr

def mock_process_text_chat(message, chat_history, personality_input):
    """Mock text chat processing"""
    if message.strip():
        personality = personality_input if personality_input.strip() else "general assistant"
        
        # Mock responses based on personality
        mock_responses = {
            "doctor": f"As your medical assistant, regarding '{message}': I'd recommend consulting with a healthcare professional for proper guidance.",
            "lawyer": f"From a legal perspective on '{message}': This is general information only - please consult an attorney for specific advice.",
            "receptionist": f"Thank you for your inquiry about '{message}'. I'll be happy to assist you with this request.",
            "teacher": f"Great question about '{message}'! Let me explain this in an educational way...",
            "therapist": f"I understand you're asking about '{message}'. I'm here to provide supportive guidance...",
        }
        
        response = mock_responses.get(personality.lower(), f"As your {personality}, I'll help you with '{message}' using my specialized expertise.")
        chat_history.append([message, response])
    
    return "", chat_history

# Setup UI mockup
with gr.Blocks(title="Personality Assistant Changer") as demo:
    gr.Markdown("<h1 style='color: orange; text-align: center; font-size: 4em;'> 🤖 Your Personal AI Assistant</h1>")
    
    # Personality Configuration Section
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 🎭 Assistant Personality")
            personality_input = gr.Textbox(
                label="What kind of assistant do you need?",
                placeholder="E.g., doctor, lawyer, receptionist, teacher, therapist, or describe your own...",
                value="general assistant",
                lines=1
            )
            gr.Markdown("*Pre-defined personalities: doctor, lawyer, receptionist, teacher, therapist*")

    with gr.Row():
        # Left column - Webcam (mockup)
        with gr.Column(scale=1):
            gr.Markdown("## 📹 Webcam Feed")
            
            with gr.Row():
                start_btn = gr.Button("Start Camera", variant="primary")
                stop_btn = gr.Button("Stop Camera", variant="secondary")
            
            # Mock webcam display
            gr.Markdown("*📷 Webcam feed would appear here (640x480)*")
            gr.Markdown("*Used for visual analysis and questions that require seeing*")
        
        # Right column - Chat
        with gr.Column(scale=1):
            gr.Markdown("## 💬 Chat Interface")
            
            chatbot = gr.Chatbot(
                label="Conversation",
                height=350,
                show_label=False,
                placeholder="Start chatting with your personalized assistant!"
            )
            
            # Text input for manual chat
            with gr.Row():
                text_input = gr.Textbox(
                    placeholder="Type your message here...",
                    lines=1,
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            gr.Markdown("*🎤 Or use continuous listening mode by clicking 'Start Voice Chat' below*")
            
            with gr.Row():
                start_voice_btn = gr.Button("Start Voice Chat", variant="primary")
                clear_btn = gr.Button("Clear Chat", variant="secondary")
    
    # Add some example interactions
    gr.Markdown("""
    ## 🎯 Quick Examples
    
    **Try different personalities:**
    1. Set personality to "doctor" and ask: "What are signs of stress?"
    2. Set personality to "lawyer" and ask: "What should I know about contracts?"
    3. Set personality to "chef" and ask: "How do I make pasta?"
    4. Set personality to "personal trainer" and ask: "What's a good workout routine?"
    """)

    # Event handlers
    text_input.submit(
        fn=mock_process_text_chat,
        inputs=[text_input, chatbot, personality_input],
        outputs=[text_input, chatbot]
    )
    
    send_btn.click(
        fn=mock_process_text_chat,
        inputs=[text_input, chatbot, personality_input],
        outputs=[text_input, chatbot]
    )
    
    clear_btn.click(
        fn=lambda: [],
        outputs=chatbot
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )