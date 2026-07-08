from youtube_transcript_api import YouTubeTranscriptApi

def transcript_download(video_id):
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(
    video_id,
    languages=["hi", "en"]
)

    transcript_data = transcript.to_raw_data()

    text = " ".join(snippet.text for snippet in transcript)
    return text
