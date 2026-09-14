import speech_recognition as sr

def listen_for_crop_input():
    """Listens for voice input and returns the recognized crop name."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for crop input...")
        audio = recognizer.listen(source)

    try:
        crop_name = recognizer.recognize_google(audio)
        print(f"You said: {crop_name}")
        return crop_name
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def listen_for_quantity_input():
    """Listens for voice input and returns the recognized quantity."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for quantity input...")
        audio = recognizer.listen(source)

    try:
        quantity = recognizer.recognize_google(audio)
        print(f"You said: {quantity}")
        return quantity
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None