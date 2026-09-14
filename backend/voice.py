from __future__ import annotations

from io import BytesIO

import streamlit as st

from .config import google_speech_api_key

try:
    import speech_recognition as sr
except ImportError:
    sr = None


LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Bengali": "bn-IN",
    "Any other language": "en-IN",
}

CROP_WORDS = {
    "tomato": "Tomato", "టమాటా": "Tomato", "tamatar": "Tomato",
    "chilli": "Chilli", "chili": "Chilli", "mirchi": "Chilli", "మిర్చి": "Chilli",
    "rice": "Rice", "paddy": "Rice", "biyyam": "Rice", "బియ్యం": "Rice",
    "cotton": "Cotton", "kapas": "Cotton", "పత్తి": "Cotton",
    "wheat": "Wheat", "gehun": "Wheat", "గోధుమ": "Wheat",
}


def render_voice_input() -> str:
    """Capture browser audio and transcribe it with the selected language."""
    language_name = st.selectbox("Voice language", list(LANGUAGES), index=2, key="voice_language")
    language_code = LANGUAGES[language_name]
    if language_name == "Any other language":
        language_code = st.text_input("Google language code", value="en-IN", key="voice_language_code")
    audio = st.audio_input("Speak your crop, quantity, or location", key="farmer_audio")
    if audio is None:
        st.caption("You can speak naturally. Choose a language above, then tap the microphone.")
        return ""
    if sr is None:
        st.error("Add SpeechRecognition to your environment to enable transcription.")
        return ""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio.getvalue())) as source:
            recording = recognizer.record(source)
        result = recognizer.recognize_google(
            recording,
            key=google_speech_api_key() or None,
            language=language_code,
        )
        st.success(f"Heard: {result}")
        return result
    except sr.UnknownValueError:
        st.warning("I could not understand that recording. Please try speaking a little closer to the microphone.")
    except sr.RequestError:
        st.error("Voice transcription needs an internet connection right now. You can continue by typing below.")
    except Exception as error:
        st.warning(f"This recording format could not be read: {error}")
    return ""


def crop_from_voice(text: str) -> str | None:
    lowered = text.casefold()
    for word, crop in CROP_WORDS.items():
        if word.casefold() in lowered:
            return crop
    return None