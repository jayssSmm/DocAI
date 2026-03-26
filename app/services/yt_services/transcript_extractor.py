from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        return url.split("v=")[-1].split("&")[0].split("?")[0]
    return url

def get_transcript(video_url):
    video_id = extract_video_id(video_url)

    yt = YouTubeTranscriptApi()
    fetched = yt.fetch(video_id)
    raw_data = fetched.to_raw_data()

    full_text = " ".join(item["text"] for item in raw_data)
    return full_text
