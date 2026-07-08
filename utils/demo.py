import streamlit as st
from youtube import transcript_download

video_id = st.text_input('Enter video id')

if st.button("Download"):
    text = transcript_download(video_id)
    st.markdown(text)