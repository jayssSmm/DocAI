from services.yt_services import transcript_extractor

a=input("link = ")
yt_link = transcript_extractor.extract_video_id(a)
rest = transcript_extractor.extract_rest_prompt(a)
print(yt_link)
print(rest)
#print(transcript_extractor.get_transcript(a))