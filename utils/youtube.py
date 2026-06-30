from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def download_transcript(video_id, output_filename="transcript.txt"):
    try:
        # 1. Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # 2. Format it into plain text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript)
        
        # 3. Save it to a file
        with open(output_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(text_formatted)
            
        print(f"✅ Transcript successfully saved to {output_filename}")
        
    except Exception as e:
        print(f"❌ Could not download transcript: {e}")

# Usage
video_id = "0dUdnlAps9Q" # Replace with your target video ID
download_transcript(video_id, f"{video_id}_transcript.txt")