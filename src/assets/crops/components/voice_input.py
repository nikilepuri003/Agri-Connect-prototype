import streamlit as st

try:
    import speech_recognition as sr
except ImportError:
    sr = None


def get_voice_input():
    """
    Capture voice input from the user's microphone
    and convert it to text.
    """

    if sr is None:
        st.error(
            "SpeechRecognition is not installed. "
            "Run: pip install SpeechRecognition"
        )
        return ""

    if not hasattr(sr, "Microphone"):
        st.warning("Voice input is unavailable because PyAudio is not installed.")
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        st.info("🔄 Converting speech to text...")

        text = recognizer.recognize_google(audio)

        st.success(f"🗣️ You said: {text}")

        return text

    except sr.WaitTimeoutError:
        st.warning("No speech detected.")
        return ""

    except sr.UnknownValueError:
        st.warning("Could not understand the audio.")
        return ""

    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
        return ""

    except Exception as e:
        st.error(f"Voice input error: {e}")
        return ""


def display_voice_input():
    """
    Streamlit UI component for voice input.
    """

    st.subheader("🎤 Voice Input")

    if st.button("🎙️ Start Voice Input"):
        text = get_voice_input()

        if text:
            st.session_state["voice_input"] = text

    return st.session_state.get("voice_input", "")