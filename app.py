import streamlit as st
import sys
import os


from utils.youtube import transcript_download

# Page config
st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .main-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
    }

    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .header p {
        font-size: 1.1em;
        opacity: 0.9;
    }

    .input-section {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }

    .input-section label {
        font-weight: 600;
        color: #333;
        display: block;
        margin-bottom: 12px;
    }

    .input-wrapper {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }

    .input-wrapper input {
        flex: 1;
        padding: 12px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 1em;
    }

    .input-wrapper button {
        padding: 12px 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: transform 0.2s;
    }

    .input-wrapper button:hover {
        transform: translateY(-2px);
    }

    .content-wrapper {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 25px;
        margin-bottom: 30px;
    }

    .chat-section {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
    }

    .section-header {
        padding: 20px;
        border-bottom: 2px solid #f0f0f0;
        font-weight: 600;
        color: #333;
        font-size: 1.1em;
    }

    .chat-messages {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        max-height: 400px;
        background: #fafafa;
    }

    .message {
        margin-bottom: 15px;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-msg {
        text-align: right;
    }

    .user-msg .bubble {
        background: #667eea;
        color: white;
        padding: 12px 15px;
        border-radius: 12px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        border-bottom-right-radius: 4px;
    }

    .ai-msg {
        text-align: left;
    }

    .ai-msg .bubble {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 12px 15px;
        border-radius: 12px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        border-bottom-left-radius: 4px;
        border-left: 4px solid #4caf50;
    }

    .chat-input-wrapper {
        padding: 15px;
        border-top: 2px solid #f0f0f0;
        display: flex;
        gap: 10px;
    }

    .chat-input-wrapper input {
        flex: 1;
        padding: 10px 12px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 1em;
    }

    .chat-input-wrapper button {
        padding: 10px 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: transform 0.2s;
    }

    .chat-input-wrapper button:hover {
        transform: translateY(-2px);
    }

    .sidebar-section {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 25px;
    }

    .sidebar-header {
        text-align: center;
        margin-bottom: 20px;
    }

    .sidebar-header h2 {
        color: #333;
        margin-bottom: 10px;
    }

    .sidebar-header p {
        color: #666;
        font-size: 0.9em;
    }

    .stats-container {
        display: grid;
        gap: 15px;
        margin-bottom: 25px;
    }

    .stat-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }

    .stat-number {
        font-size: 2em;
        font-weight: 700;
        color: #667eea;
        display: block;
    }

    .stat-label {
        color: #666;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .suggestions {
        display: grid;
        gap: 10px;
    }

    .suggestion {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 12px 15px;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9em;
    }

    .suggestion:hover {
        background: #e9ecef;
        transform: translateY(-2px);
        border-color: #667eea;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 0;
    }

    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #28a745;
    }

    .status-text {
        color: #666;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Header
st.markdown("""
<div class="main-container">
    <div class="header">
        <h1>YouTube RAG Chatbot</h1>
        <p>Chat with any YouTube video using AI</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown('<label for="youtube-url">Enter YouTube VideoID</label>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    video_id = st.text_input(
        label="video id",
        placeholder="",
        label_visibility="collapsed"
    )
with col2:
    process_button = st.button("Process Video", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Process video when button is clicked
if process_button and video_id:
    with st.spinner("Processing video..."):
        # Extract video ID and download transcript
        transcript_text = transcript_download(video_id)
        st.markdown(transcript_text)