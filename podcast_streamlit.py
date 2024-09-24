import streamlit as st
from gtts import gTTS
import io
import base64
from newspaper import Article
import pathlib
import pandas as pd
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def text_to_speech(text):
  audio = gTTS(text, lang='en', slow=False, tld='co.in')
  speech_bytes = io.BytesIO()
  audio.write_to_fp(speech_bytes)
  return speech_bytes


def podcast(news_url, counter):

    news = Article(news_url)
    news.download()
    news.parse()
    news.nlp()
    
    news_sr = f"News number - {counter}"
    news_title = news.title
    news_text = news.text
    news_summary = summarizer(news_text, max_length=300, min_length=100, do_sample=False)

    return " \n".join([news_sr, news_title, news_summary[0]['summary_text']])


def single_url_input(news_url):
  
  news = Article(news_url)
  news.download()
  news.parse()
  news.nlp()
  
  news_title = news.title
  news_text = news.text
  news_summary = summarizer(news_text, max_length=300, min_length=100, do_sample=False)
#   print(news_summary[0]['summary_text'])

#   final_text =  " \n".join([news_title, news_summary])

  return news_summary[0]['summary_text']
  
  

def file_upload_input(file):
    
    df = pd.read_csv(file)

    news_list = []

    counter = 1

    for url in df.url_link:

        news_list.append(podcast(url, counter))
        counter = counter + 1

    final_text = " \n".join(news_list)

    return final_text



def main():
    
    st.title("Library Podcast")

    # Single URL input
    st.subheader("Single Article Podcast")

    user_input = st.text_area("Enter the URL of the article you want to convert to speech:",
                                height=150)

    
    # Convert button
    if st.button("Convert to Speech"):

        final_text = single_url_input(user_input)

        st.markdown(final_text)

        speech_bytes = text_to_speech(final_text)
        
        st.audio(speech_bytes, format="audio/mp3")
        st.download_button(label="Download Speech",
                        data=speech_bytes,
                        file_name="speech.mp3",
                        mime="audio/mp3")
        
    
    # Multiple URLs input
    st.subheader("Capturing multiple URLs from the file")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        
        final_text = file_upload_input(uploaded_file)

        st.markdown(final_text)

    if st.button("Convert to speech"):

        speech_bytes = text_to_speech(final_text)
        
        st.audio(speech_bytes, format="audio/mp3")
        st.download_button(label="Download Speech",
                        data=speech_bytes,
                        file_name="speech.mp3",
                        mime="audio/mp3")
        

if __name__ == "__main__":
  main()
