import streamlit as st
from dotenv import load_dotenv
import os
import time
import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Using Groq API Key

# Groq Cloud API details
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"  # Smaller model to avoid token limit issues

# Summarization prompt
PROMPT = """You are a YouTube video summarizer. Summarize the entire video in **less than 250 words**, 
providing key points concisely. Format the summary using bullet points.  
Here is the transcript: 
"""

# Function to extract YouTube transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[-1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# Function to split transcript into smaller chunks
def split_text(text, chunk_size=1000):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to generate summary using Groq Cloud API
def generate_groq_summary(transcript_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    transcript_chunks = split_text(transcript_text)  # Split transcript into parts
    summaries = []

    for chunk in transcript_chunks:
        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are an expert summarizer."},
                {"role": "user", "content": PROMPT + chunk}
            ],
            "temperature": 0.7
        }

        while True:
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
            response_json = response.json()

            # Handle rate limits
            if "error" in response_json and "rate_limit_exceeded" in response_json["error"].get("code", ""):
                wait_time = int(response_json["error"].get("message", "").split("in ")[-1].split("s")[0])
                st.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time + 1)  # Wait before retrying
            else:
                break

        if "choices" in response_json:
            summaries.append(response_json["choices"][0]["message"]["content"])
        else:
            return f"❌ API Error: {response_json}"

    return "\n\n".join(summaries)  # Combine all summaries

# Streamlit UI
st.title("🎥 YouTube Transcript to Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[-1].split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        with st.spinner("Generating summary..."):
            summary = generate_groq_summary(transcript_text)
        st.markdown("## 📌 Detailed Notes:")
        st.write(summary)
    else:
        st.error("❌ Could not retrieve transcript. The video may not have captions.")
