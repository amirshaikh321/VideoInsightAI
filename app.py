import streamlit as st

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
        font-size: 0.95em;
    }
    
    .chat-input-wrapper button {
        padding: 10px 20px;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: background 0.2s;
    }
    
    .chat-input-wrapper button:hover {
        background: #764ba2;
    }
    
    .source-section {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
    }
    
    .source-list {
        padding: 20px;
        overflow-y: auto;
        max-height: 500px;
    }
    
    .source-chunk {
        background: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 4px solid #ff9800;
        font-size: 0.95em;
        line-height: 1.5;
        color: #5d4037;
    }
    
    .source-chunk strong {
        display: block;
        margin-bottom: 8px;
        color: #e65100;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #999;
    }
    
    .empty-state svg {
        width: 60px;
        height: 60px;
        margin-bottom: 15px;
        opacity: 0.5;
    }
    
    @media (max-width: 900px) {
        .content-wrapper {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "What is CNN?"},
        {"role": "assistant", "content": "CNN stands for Convolutional Neural Network. It is a deep learning algorithm used primarily for image processing and computer vision tasks. CNNs use convolutional layers to automatically learn spatial hierarchies of features from input images."},
    ]

if 'source_chunks' not in st.session_state:
    st.session_state.source_chunks = [
        "Chunk 1: CNNs are composed of neurons that each have a learnable weight and bias. Each neuron receives some inputs, performs a dot product, and optionally follows it with a nonlinearity...",
        "Chunk 2: The key characteristic of a convolutional layer is that all neurons in a layer share the same weights and bias. This reduces the number of parameters and computations...",
        "Chunk 3: Pooling layers serve to progressively reduce the spatial size of the representation to reduce the amount of parameters and computation in the network...",
    ]

# Header
st.markdown("""
<div class="header">
    <h1>🎥 YouTube RAG Chatbot</h1>
    <p>Extract knowledge from YouTube videos</p>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("""
<div class="input-section">
    <label>Enter YouTube URL</label>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    url_input = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

with col2:
    if st.button("Process Video", use_container_width=True):
        st.success("✅ Video processed successfully!")

# Main Content Grid
col_chat, col_source = st.columns([1.5, 1])

# Chat Section
with col_chat:
    st.markdown("""
    <div class="chat-section">
        <div class="section-header">💬 Chat</div>
        <div class="chat-messages">
    """, unsafe_allow_html=True)
    
    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-msg">
                <div class="bubble">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message ai-msg">
                <div class="bubble">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input
    st.markdown("""
    <div class="chat-input-wrapper">
    """, unsafe_allow_html=True)
    
    col_input, col_btn = st.columns([5,1])
    with col_input:
        user_input = st.text_input("", placeholder="Ask a question...", label_visibility="collapsed", key="chat_input")
    
    with col_btn:
        if st.button("Send", use_container_width=True):
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": "This is a sample response based on the video content. The actual response will be generated from the video transcript using RAG."})
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
