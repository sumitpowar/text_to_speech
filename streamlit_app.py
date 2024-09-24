import streamlit as st
from gtts import gTTS
import io
import base64
from newspaper import Article
import pathlib
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/sumitpowar/text_to_speech/refs/heads/master/url_list.csv')

def podcast(news_url):
  news = Article(news_url)
  news.download()
  news.parse()
  news.nlp()

  news_text = news.text
  news_summary = news.summary
  
  return news_summary

def text_to_speech(text):
  audio = gTTS(text, lang='en', slow=False, tld='co.in')
  speech_bytes = io.BytesIO()
  audio.write_to_fp(speech_bytes)
  return speech_bytes


def main():
  st.title("Library Podcast")

  # Text input
  user_input = st.text_area("Enter the text you want to convert to speech:",
                            height=150)

  
  # Convert button
  if st.button("Convert to Speech"):
    speech_bytes = text_to_speech(user_input)
    
    st.audio(speech_bytes, format="audio/mp3")
    st.download_button(label="Download Speech",
                       data=speech_bytes,
                       file_name="speech.mp3",
                       mime="audio/mp3")

if __name__ == "__main__":
  main()
