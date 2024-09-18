import streamlit as st
from gtts import gTTS
import io
import base64

def text_to_speech(text):
  audio = gTTS(text, lang='en')
  speech_bytes = io.BytesIO()
  
  return audio.write_to_fp(speech_bytes)


def main():
  st.title("Library Podcast")

  # Text input
  user_input = st.text_area("Enter the text you want to convert to speech:",
                            height=150)

  
  # Convert button
  if st.button("Convert to Speech"):
    audio_bytes = text_to_speech(user_input)
    
    st.audio(audio_bytes, format='audio/mp3')
    # st.download_button(label="Download Speech",
    #                    data=audio_bytes,
    #                    file_name="speech.mp3",
    #                    mime="audio/mp3")

if __name__ == "__main__":
  main()
