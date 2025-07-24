import cv2
import base64
from dotenv import load_dotenv

load_dotenv()

def capture_image() -> str:
    """
    Captures one frame from the default webcam, resizes it,
    encodes it as Base64 JPEG (raw string) and returns it.
    """
    for idx in range(4):
        cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            for _ in range(10):  # Warm up
                cap.read()
            ret, frame = cap.read()
            cap.release()
            if not ret:
                continue
            cv2.imwrite("sample.jpg", frame)  # Optional
            ret, buf = cv2.imencode('.jpg', frame)
            if ret:
                return base64.b64encode(buf).decode('utf-8')
    raise RuntimeError("Could not open any webcam (tried indices 0-3)")


from groq import Groq

def analyze_image_with_query(query: str) -> str:
    """
    Expects a string with 'query'.
    Captures the image and sends the query and the image to
    to Groq's vision chat API and returns the analysis.
    Enhanced to provide detailed observations for compliments.
    """
    img_b64 = capture_image()
    model="meta-llama/llama-4-maverick-17b-128e-instruct"
    
    if not query or not img_b64:
        return "Error: both 'query' and 'image' fields required."

    client=Groq()  
    
    # Enhanced prompt to encourage detailed positive observations
    enhanced_query = f"""
    {query}
    
    Please provide detailed observations about:
    - The person's appearance, clothing style, and professional presentation
    - Any positive qualities or attractive features you notice
    - Their expression, confidence, or energy that comes through
    - The background or environment that might indicate their interests
    - Overall impression of their style, professionalism, or personality
    
    Be specific and positive in your observations while being genuine and appropriate.
    """
    
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": enhanced_query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content

#query = "How many people do you see?"
#print(analyze_image_with_query(query))