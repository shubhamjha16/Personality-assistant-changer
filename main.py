import os
import gradio as gr
from speech_to_text import record_audio, transcribe_with_groq
from ai_agent import ask_agent, set_custom_prompt
from text_to_speech import text_to_speech_with_elevenlabs, text_to_speech_with_gtts

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
audio_filepath = "audio_question.mp3"

def process_audio_and_chat(personality, custom_prompt=""):
    # Handle custom personality
    if personality.lower() == "custom" and custom_prompt.strip():
        set_custom_prompt(custom_prompt.strip())
    
    chat_history = []
    while True:
        try:
            record_audio(file_path=audio_filepath)
            user_input = transcribe_with_groq(audio_filepath)

            if "goodbye" in user_input.lower():
                break

            response = ask_agent(user_query=user_input, personality=personality)

            voice_of_doctor = text_to_speech_with_elevenlabs(input_text=response, output_filepath="final.mp3")

            chat_history.append([user_input, response])

            yield chat_history

        except Exception as e:
            print(f"Error in continuous recording: {e}")
            break

def toggle_custom_prompt(personality):
    """Show/hide custom prompt input based on personality selection."""
    return gr.update(visible=(personality == "Custom"))

# Code for frontend
import cv2
# Global variables
camera = None
is_running = False
last_frame = None

def initialize_camera():
    """Initialize the camera with optimized settings"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            # Optimize camera settings for better performance
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_FPS, 30)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to minimize lag
    return camera is not None and camera.isOpened()

def start_webcam():
    """Start the webcam feed"""
    global is_running, last_frame
    is_running = True
    if not initialize_camera():
        return None
    
    ret, frame = camera.read()
    if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = frame
        return frame
    return last_frame

def stop_webcam():
    """Stop the webcam feed"""
    global is_running, camera
    is_running = False
    if camera is not None:
        camera.release()
        camera = None
    return None

def get_webcam_frame():
    """Get current webcam frame with optimized performance"""
    global camera, is_running, last_frame
    
    if not is_running or camera is None:
        return last_frame
    
    # Skip frames if buffer is full to avoid lag
    if camera.get(cv2.CAP_PROP_BUFFERSIZE) > 1:
        for _ in range(int(camera.get(cv2.CAP_PROP_BUFFERSIZE)) - 1):
            camera.read()
    
    ret, frame = camera.read()
    if ret and frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = frame
        return frame
    return last_frame

# Setup UI

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='color: orange; text-align: center;  font-size: 4em;'> 👧🏼 Dora – Your Personal AI Assistant</h1>")
    
    # Personality Selector
    with gr.Row():
        personality_selector = gr.Dropdown(
            choices=["General Assistant", "Doctor", "Lawyer", "Receptionist", "Teacher", "Chef", "Custom"],
            value="General Assistant",
            label="Assistant Personality",
            info="Select what kind of assistant you need"
        )
    
    # Custom prompt input (initially hidden)
    custom_prompt_input = gr.Textbox(
        label="Custom Personality Description",
        placeholder="Describe the personality you want (e.g., 'a helpful business consultant who specializes in marketing strategies')",
        visible=False,
        lines=3
    )

    with gr.Row():
        # Left column - Webcam
        with gr.Column(scale=1):
            gr.Markdown("## Webcam Feed")
            
            with gr.Row():
                start_btn = gr.Button("Start Camera", variant="primary")
                stop_btn = gr.Button("Stop Camera", variant="secondary")
            
            webcam_output = gr.Image(
                label="Live Feed",
                streaming=True,
                show_label=False,
                width=640,
                height=480
            )
            
            # Faster refresh rate for smoother video
            webcam_timer = gr.Timer(0.033)  # ~30 FPS (1/30 ≈ 0.033 seconds)
        
        # Right column - Chat
        with gr.Column(scale=1):
            gr.Markdown("## Chat Interface")
            
            chatbot = gr.Chatbot(
                label="Conversation",
                height=400,
                show_label=False
            )
            
            gr.Markdown("*🎤 Continuous listening mode is active - speak anytime!*")
            
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
    
    # Event handlers
    start_btn.click(
        fn=start_webcam,
        outputs=webcam_output
    )
    
    stop_btn.click(
        fn=stop_webcam,
        outputs=webcam_output
    )
    
    webcam_timer.tick(
        fn=get_webcam_frame,
        outputs=webcam_output,
        show_progress=False  # Hide progress indicator for smoother experience
    )
    
    clear_btn.click(
        fn=lambda: [],
        outputs=chatbot
    )
    
    # Show/hide custom prompt when personality changes
    personality_selector.change(
        fn=toggle_custom_prompt,
        inputs=personality_selector,
        outputs=custom_prompt_input
    )
    
    # Restart continuous mode when personality changes
    personality_selector.change(
        fn=process_audio_and_chat,
        inputs=[personality_selector, custom_prompt_input],
        outputs=chatbot
    )
    
    # Update when custom prompt changes
    custom_prompt_input.change(
        fn=process_audio_and_chat,
        inputs=[personality_selector, custom_prompt_input],
        outputs=chatbot
    )
    
    # Auto-start continuous mode when the app loads
    demo.load(
        fn=process_audio_and_chat,
        inputs=[personality_selector, custom_prompt_input],
        outputs=chatbot
    )

## Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )
