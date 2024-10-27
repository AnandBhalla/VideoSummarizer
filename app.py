import google.generativeai as genai
import streamlit as st
from pytube import YouTube
import os
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
load_dotenv()

genai_api_key = st.secrets["GENAI_API_KEY"]
genai.configure(api_key=genai_api_key)


def generate_transcript(url):
    video_id=url.split('=')[1]
    transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ""
    for i in transcript_text:
        transcript += " " + i["text"]
    return transcript

def generate_output(transcript):
    prompt = st.secrets["PROMPT"]
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt+transcript)
    return response.text

st.title("YouTube Video Summarizer")
youtube_url = st.text_input("Enter the YouTube Video URL")

if youtube_url:
        yt = YouTube(youtube_url)
        st.image(yt.thumbnail_url, caption="Video Thumbnail", use_column_width=True)
        if st.button("Summarize Video"):
            transcript = generate_transcript(youtube_url)
            output = generate_output(transcript)
            st.header("Video Summary")
            st.write(output)
else:
    st.write("Please enter a valid YouTube URL.")