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

# 🎨 Custom CSS Styles
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton button {
        background-color: #ff4b4b !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 10px;
    }
    .stDownloadButton button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🌟 Header
st.markdown("<h1 style='text-align: center;'>🎙️ VoicePersona: AI-Powered Text-to-Speech</h1>", unsafe_allow_html=True)
st.write("🎧 **Convert your text into expressive speech with various voice personas!**")

# 📜 Text Input Section
st.markdown("### ✍️ Enter Your Text:")
text_input = st.text_area("", "Hello, welcome to VoicePersona!", height=150)

# 🎭 Persona Selection
st.markdown("### 🎭 Choose a Voice Persona:")
selected_persona = st.selectbox("", list(VOICE_PERSONAS.keys()))

# 🎚 Sidebar for Custom Settings
st.sidebar.header("⚙️ Voice Customization")
pitch = st.sidebar.slider("🎵 Adjust Pitch", -20.0, 20.0, VOICE_PERSONAS[selected_persona]["pitch"])
speed = st.sidebar.slider("⏩ Adjust Speed", 0.5, 2.0, VOICE_PERSONAS[selected_persona]["speaking_rate"])

# 🚀 Generate Button
if st.button("🎙️ Generate Audio"):
    if text_input.strip():
        # Progress Bar
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

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
            pitch=pitch,
            speaking_rate=speed
        )

        # Generate speech
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Convert to audio buffer
        audio_buffer = BytesIO(response.audio_content)

        # 🎵 Play the generated audio
        st.audio(audio_buffer, format="audio/mp3")

        # 📥 Download Option
        st.download_button(
            label="📥 Download Audio",
            data=audio_buffer,
            file_name="voicepersona_audio.mp3",
            mime="audio/mp3"
        )

    else:
        st.warning("⚠️ Please enter text before generating audio.")
