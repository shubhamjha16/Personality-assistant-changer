# 🤖 Personality Assistant Changer

Your new AI assistant that can dynamically change its personality based on your needs! Whether you need a doctor, lawyer, receptionist, teacher, therapist, or any custom role, this assistant adapts to provide specialized expertise and communication style.

## ✨ Key Features

- **🎭 Dynamic Personality System**: Switch between different assistant personalities on demand
- **😊 Enthusiastic & Complimentary**: AI that genuinely compliments your appearance, style, and professional qualities
- **🎥 Real-time Webcam Integration**: Visual analysis capabilities with appearance-based compliments
- **🎙️ Voice Interaction**: Speak naturally and get audio responses
- **💬 Text Chat**: Type messages for quick interactions
- **🔧 Customizable Roles**: Use predefined personalities or create your own
- **⚡ Vercel Deployment Ready**: Easy cloud deployment with included configuration

## 🎯 Supported Personalities

### Professional Commanding Personalities
Each personality takes charge of conversations with professional authority and actively engages users through systematic questioning, while being enthusiastic and complimentary:

- **🩺 Doctor**: Conducts medical consultations with diagnostic questioning, symptom assessment, health recommendations, and caring compliments about taking charge of health
- **⚖️ Lawyer**: Leads legal consultations gathering case details, analyzing situations, providing strategic advice, and appreciating client intelligence and preparation  
- **📞 Receptionist**: Manages appointments and administrative tasks through organized questioning, efficient service, and warm welcomes with appearance compliments
- **📚 Teacher**: Conducts interactive lessons with knowledge testing, confidence assessment, personalized feedback, and enthusiastic encouragement about learning dedication
- **🧠 Therapist**: Guides therapeutic sessions through professional questioning, emotional support techniques, and genuine compliments about courage in seeking help
- **💼 HR Manager**: Conducts structured interviews with behavioral questions, comprehensive candidate evaluation, balanced feedback including both strengths and areas for improvement

### Interactive Professional Behaviors
All personalities demonstrate commanding professional conduct with enthusiasm:
- **Take Charge**: Lead conversations instead of waiting for user direction
- **Active Questioning**: Immediately ask relevant questions to gather comprehensive information
- **Professional Assessment**: Evaluate responses and provide expert feedback
- **Role-Specific Interactions**: Engage in activities typical of their profession (tests, interviews, consultations)
- **Enthusiastic Compliments**: Use webcam to give genuine compliments about appearance, style, and professional presentation
- **Genuine Interest**: Show authentic care about the person's goals, background, and wellbeing

### Custom Personalities
Create any specialized professional by describing the role. Custom personalities automatically adopt commanding behavior:
- Software Engineer
- Chef
- Personal Trainer
- Travel Guide
- Financial Advisor
- Marketing Expert
- And many more!

## 🚀 Quick Start

### Prerequisites
Make sure you have the following API keys set up as environment variables:
- `GROQ_API_KEY`: For speech-to-text and AI processing
- `ELEVENLABS_API_KEY`: For text-to-speech (optional)
- `GOOGLE_API_KEY`: For the Gemini AI model

### Installation

**Option A: Local Development**

1. **Clone the repository:**
```bash
git clone https://github.com/shubhamjha16/Personality-assistant-changer.git
cd Personality-assistant-changer
```

2. **Install dependencies:**

**Using UV (Recommended)**
```bash
# Setup UV if not already: https://www.youtube.com/watch?v=Dgf7Lp0B_hI
uv sync
```

**Using pip**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

4. **Run the application:**
```bash
python main.py
```

**Option B: Deploy to Vercel**

1. **Deploy to Vercel:**
   - Fork this repository
   - Connect to Vercel
   - Add environment variables in Vercel dashboard:
     - `GROQ_API_KEY`
     - `ELEVENLABS_API_KEY` 
     - `GOOGLE_API_KEY`
   - Deploy automatically

2. **Vercel Configuration:**
   The repository includes `vercel.json` and `requirements.txt` for seamless deployment.

## 🎮 How to Use

1. **Launch the application** by running `python main.py`
2. **Set the personality** in the "What kind of assistant do you need?" field
   - Enter predefined personalities: `doctor`, `lawyer`, `receptionist`, `teacher`, `therapist`
   - Or create custom roles: `chef`, `marketing expert`, `game developer`, etc.
3. **Start interacting** using either:
   - **Text chat**: Type messages and click Send
   - **Voice chat**: Click "Start Voice Chat" for continuous voice interaction
4. **Enable webcam** if you need visual analysis capabilities

## 🧪 Testing

Run the personality system tests:
```bash
# Test personality prompt generation
python test_personality_simple.py

# See personality demo
python demo_personality.py
```

## 📁 Project Structure

```
├── main.py                 # Main Gradio UI application
├── ai_agent.py            # Core AI agent with personality system
├── speech_to_text.py      # Voice input processing
├── text_to_speech.py      # Voice output generation
├── tools.py               # Webcam and image analysis tools
├── demo_personality.py    # Personality system demonstration
└── test_personality_simple.py  # Test suite
```

## 🔧 Technical Details

### Personality System
The personality system works by:
1. **Dynamic Prompt Generation**: Each personality type generates a specialized system prompt
2. **Context Awareness**: Maintains role-appropriate boundaries and expertise
3. **Flexible Architecture**: Easy to add new personalities or modify existing ones

### Core Components
- **AI Agent**: Uses Gemini 2.0 Flash model with LangGraph
- **Speech Processing**: Groq Whisper for speech-to-text
- **Voice Synthesis**: ElevenLabs for natural voice output
- **Vision**: Webcam integration for visual queries
- **UI**: Gradio for intuitive web interface

## 🎥 Video Tutorial

▶️ **Watch the Setup Video**  
🎥 [How to Get Started with This Project](https://www.youtube.com/watch?v=0ascQRbv7Kk)

## 🤝 Contributing

Feel free to contribute by:
- Adding new predefined personalities
- Improving the personality prompt templates
- Enhancing the UI/UX
- Adding new features

## 📄 License

This project is open source. Feel free to use and modify as needed.