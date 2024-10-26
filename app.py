import google.generativeai as genai
import streamlit as st
from pytube import YouTube
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, VideoUnavailable
from dotenv import load_dotenv
load_dotenv()




def generate_transcript(url):
    video_id = url.split('v=')[-1]
    amp_index = video_id.find('&')
    if amp_index != -1:
        video_id = video_id[:amp_index]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
    text = "\n".join([entry['text'] for entry in transcript])
    return text.strip()

def generate_output(transcript):
    genai_api_key = st.secrets["GENAI_API_KEY"]
    prompt = st.secrets["PROMPT"]
    # genai.configure(api_key=os.getenv("GENAI_API_KEY"))
    genai.configure(api_key=genai_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    # prompt=os.getenv("PROMPT")
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