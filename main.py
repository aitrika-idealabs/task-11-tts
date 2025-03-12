import streamlit as st
import os
import json
from google.cloud import texttospeech
from io import BytesIO
import time  # For progress bar

# Load Google Cloud credentials from secrets
credentials = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_tts_credentials.json"

with open("google_tts_credentials.json", "w") as f:
    json.dump(credentials, f)

# Initialize Google Cloud TTS client
client = texttospeech.TextToSpeechClient()

# Define voice personas with modulation settings
VOICE_PERSONAS = {
    "🎙️ Professional Narrator": {"voice_name": "en-US-Wavenet-D", "pitch": 0.0, "speaking_rate": 1.0},
    "🧑‍🏫 Friendly Coach": {"voice_name": "en-US-Wavenet-F", "pitch": 0.5, "speaking_rate": 1.1},
    "🎤 Enthusiastic Presenter": {"voice_name": "en-US-Wavenet-G", "pitch": 1.0, "speaking_rate": 1.2},
    "📖 Calm Storyteller": {"voice_name": "en-US-Wavenet-E", "pitch": -0.5, "speaking_rate": 0.9},
    "📰 Serious News Anchor": {"voice_name": "en-US-Wavenet-A", "pitch": -0.2, "speaking_rate": 1.0},
    "🤖 AI Assistant": {"voice_name": "en-US-Standard-C", "pitch": 0.0, "speaking_rate": 1.0},
    "👶 Playful Kid": {"voice_name": "en-US-Wavenet-H", "pitch": 1.5, "speaking_rate": 1.3},
    "👴 Elderly Mentor": {"voice_name": "en-US-Wavenet-I", "pitch": -1.0, "speaking_rate": 0.8},
    "📻 Radio DJ": {"voice_name": "en-US-Wavenet-J", "pitch": 0.7, "speaking_rate": 1.2},
    "🧘 Relaxing Meditation Guide": {"voice_name": "en-US-Wavenet-K", "pitch": -0.8, "speaking_rate": 0.7},
}

# Apply enhanced CSS styling
def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f8f8fb !important;
            color: #2c3e50 !important;
            font-family: 'Inter', sans-serif !important;
        }
        .stApp { 
            background-color: #f8f8fb; 
            font-family: 'Inter', sans-serif; 
        }
        .header-container {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .st-emotion-cache-h4xjwg {
            color: #FF5C0A; 
            position: fixed;
            top: 0px;
            left: 0px;
            right: 0px;
            height: 3.75rem;
            background: rgb(248,248,248);
            outline: none;
            z-index: 999990;
            display: block;
        }
        .app-title {
            font-size: 3rem;
            font-weight: 800;
            color: #FF5C0A;
            text-align: left;
            letter-spacing: -2px;
            margin: 0;
        }
        .water-round-container {
            width: 80px;
            height: 80px;
            position: relative;
            overflow: hidden;
            border-radius: 50%;
            border: 2px solid silver;
            animation: water-waves linear 10s infinite;
        }
        .water-wave1 {
            position: absolute;
            top: 40%;
            left: -25%;
            background: #FF5C0A;
            opacity: 0.7;
            width: 200%;
            height: 200%;
            border-radius: 40%;
            animation: inherit;
            animation-duration: 5s;
        }
        .water-wave2 {
            position: absolute;
            top: 45%;
            left: -35%;
            background: #FF5C0A;
            opacity: 0.5;
            width: 200%;
            height: 200%;
            border-radius: 35%;
            animation: inherit;
            animation-duration: 7s;
        }
        .water-wave3 {
            position: absolute;
            top: 50%;
            left: -35%;
            background: #FF5C0A;
            opacity: 0.3;
            width: 200%;
            height: 200%;
            border-radius: 33%;
            animation: inherit;
            animation-duration: 11s;
        }
        @keyframes water-waves {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: #2c3e50;
            line-height: 1.2;
            margin-bottom: 1rem;
        }
        .highlight {
            color: #ff5722;
        }
        .subtitle {
            font-size: 1.25rem;
            color: #637082;
            max-width: 700px;
            margin: 0 auto 2rem;
            text-align: left;
        }
        
        /* Custom textarea styling */
        .stTextArea textarea {
            border: 2px solid rgba(255, 92, 10, 0.2);
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background-color: rgba(255, 92, 10, 0.02);
        }
        
        .stTextArea textarea:focus {
            border-color: #FF5C0A;
            box-shadow: 0 0 0 2px rgba(255, 92, 10, 0.1);
        }
        
        /* Custom selectbox styling */
        div[data-baseweb="select"] {
            border-radius: 12px;
            overflow: hidden;
            border: 2px solid rgba(255, 92, 10, 0.2);
            transition: all 0.3s ease;
        }
        
        div[data-baseweb="select"]:hover {
            border-color: #FF5C0A;
        }
        
        /* Custom slider styling */
        div[data-testid="stSlider"] {
            padding: 10px 0;
        }
        
        /* Custom button styling */
        div.stButton > button {
            background-color: #FF5C0A !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(255, 92, 10, 0.3) !important;
            transition: all 0.3s ease !important;
            font-size: 16px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(255, 92, 10, 0.4) !important;
            background-color: #FF7D3C !important;
        }

        div.stDownloadButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3) !important;
            transition: all 0.3s ease !important;
            font-size: 16px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        div.stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4) !important;
            background-color: #5BBD60 !important;
        }
        
        /* Audio player styling */
        div[data-testid="stAudio"] {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            border: 2px solid rgba(255, 92, 10, 0.2);
            margin: 15px 0;
        }
        
        /* Progress bar styling */
        div[data-testid="stProgressBar"] {
            margin: 15px 0;
        }
        
        /* Section headers */
        .section-header {
            display: inline-block;
            background-color: rgba(255, 92, 10, 0.1);
            padding: 8px 16px;
            border-radius: 20px;
            color: #FF5C0A;
            font-weight: 500;
            margin-bottom: 15px;
        }
        
        /* Card styling */
        .card-container {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
            border-left: 4px solid #FF5C0A;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply the custom CSS
apply_custom_css()

# App Header with Logo Animation
st.markdown("""
<div class="header-container">
    <div class="water-round-container">
        <div class="water-wave1"></div>
        <div class="water-wave2"></div>
        <div class="water-wave3"></div>
    </div>
    <h1 class="app-title">VoicePersona</h1>
</div>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<h2 class="hero-title">Transform text into <span class="highlight">expressive speech</span></h2>
<p class="subtitle">Create dynamic audio content with customizable voice personas for presentations, content creation, accessibility, and more.</p>
""", unsafe_allow_html=True)

# Main Content in Card Containers
# st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<div class="section-header">✍️ Enter Your Text</div>', unsafe_allow_html=True)
text_input = st.text_area("", "Hello, welcome to VoicePersona!", height=150)
st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🎭 Choose a Voice Persona</div>', unsafe_allow_html=True)
selected_persona = st.selectbox("", list(VOICE_PERSONAS.keys()))
st.markdown('</div>', unsafe_allow_html=True)

# # Sidebar for Custom Settings
# st.sidebar.markdown('<h3 style="color:#FF5C0A; font-weight:600; margin-bottom:20px;">⚙️ Voice Customization</h3>', unsafe_allow_html=True)
# st.sidebar.markdown('<div style="background-color:white; padding:20px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
# # pitch = st.sidebar.slider("🎵 Adjust Pitch", -20.0, 20.0, VOICE_PERSONAS[selected_persona]["pitch"])
# # speed = st.sidebar.slider("⏩ Adjust Speed", 0.5, 2.0, VOICE_PERSONAS[selected_persona]["speaking_rate"])
# st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Generate Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎙️ Generate Audio"):
        if text_input.strip():
            # Progress Bar
            st.markdown('<div style="margin:20px 0;">', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            st.markdown('</div>', unsafe_allow_html=True)

            # Get selected voice settings
            voice_settings = VOICE_PERSONAS[selected_persona]

            # Configure the voice request
            synthesis_input = texttospeech.SynthesisInput(text=text_input)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice_settings["voice_name"]
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                # pitch=pitch,
                # speaking_rate=speed
            )

            # Generate speech
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

            # Convert to audio buffer
            audio_buffer = BytesIO(response.audio_content)

            # Output section
            # st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🔊 Your Generated Audio</div>', unsafe_allow_html=True)
            
            # Play the generated audio
            st.audio(audio_buffer, format="audio/mp3")

            # Download Option
            st.download_button(
                label="📥 Download Audio",
                data=audio_buffer,
                file_name="voicepersona_audio.mp3",
                mime="audio/mp3"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background-color: #FFF5F5; color: #E53E3E; padding: 16px; border-radius: 8px; border-left: 4px solid #E53E3E; margin: 20px 0;">
                <strong>⚠️ Please enter text before generating audio.</strong>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: #94A3B8; font-size: 14px;">
    <p>Made with ❤️ by VoicePersona</p>
</div>
""", unsafe_allow_html=True)
