import requests
import os
from dotenv import load_dotenv

load_dotenv()

def extract_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        return url.split("v=")[-1].split("&")[0].split("?")[0]
    return url

def extract_rest_prompt(prompt):
    if "youtu.be" in prompt:
        return " ".join(prompt.split("/")[-1].split("?")[1].split()[1:])
    elif "youtube.com" in prompt:
        return " ".join(prompt.split("v=")[-1].split("&")[0].split("?")[1].split()[1:])
    return prompt


def get_transcript(url: str) -> dict:
    video_id = extract_video_id(url)
    
    response = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        params={"videoId": video_id, "text": True},
        headers={"x-api-key": os.getenv('SUPADATA_API_KEY')}
    )
    response.raise_for_status()
    response_json = response.json()

    text = " ".join([str(x['text']) for x in response_json['content']])

    return text