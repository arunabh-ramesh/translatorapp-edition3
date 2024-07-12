import streamlit as st
import speech_recognition as sr
from translate import Translator
import tempfile
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Function to translate text
def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation

# Function to detect language
def detect_language(text):
    try:
        detected_lang = detect(text)
    except LangDetectException as e:
        st.warning(f"Language detection failed: {e}")
        detected_lang = "en"  # Default to English if detection fails
    return detected_lang

# Function to perform speech recognition on uploaded audio file
def recognize_speech(audio_file):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)  # Read the entire audio file
            recognized_text = recognizer.recognize_google(audio_data)
            return recognized_text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Streamlit App
def main():
    st.title("🗣️Translator App")
    st.write("Welcome! Please enter the text you want translated.")

    # Input fields
    text = st.text_area("Text to Translate")
    
    if st.checkbox("Detect Language Automatically"):
        detected_language = detect_language(text)
        st.write(f"Detected Language: {detected_language}")
    
    language = st.selectbox(
        "Choose the Language to Translate Into", 
        ["es", "fr", "de", "zh", "ja",], 
        format_func=lambda x: {
            "es": "Spanish", 
            "fr": "French", 
            "de": "German", 
            "zh": "Chinese", 
            "ja": "Japanese"
        }[x]
    )

    if st.button("Translate"):
        if text and language:
            translation = translate_text(text, language)
            st.write("Translated Text:")
            st.write(translation)
        else:
            st.write("Please enter text and select a language before translating.")

    # Speech recognition input
    st.write("Alternatively, you can use Speech Recognition:")
    uploaded_file = st.file_uploader("Upload an audio file for speech recognition", type=["wav", "mp3", "flac", "aiff", "aif"])

    if uploaded_file:
        st.audio(uploaded_file, format='audio/wav')

        if st.button("Recognize Speech"):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_audio:
                tmp_audio.write(uploaded_file.read())
                audio_file_path = tmp_audio.name

            st.write("Processing audio...")
            recognized_text = recognize_speech(audio_file_path)
            st.write("Recognized Text:")
            st.write(recognized_text)

            # Store recognized text in a session state variable
            st.session_state.recognized_text = recognized_text

    # Option to translate recognized text
    if st.checkbox("Translate Recognized Text"):
        if "recognized_text" in st.session_state:
            if st.session_state.recognized_text:
                translation = translate_text(st.session_state.recognized_text, language)
                st.write("Translated Text:")
                st.write(translation)
            else:
                st.write("No recognized text to translate.")

if __name__ == "__main__":
    main()
