import os
from google import genai
from google.genai import types

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def response(prompt,history):

    message={'role':'user','parts':[prompt]}
    history.append(message)

    contents=[
        types.Content(role=item['role'],parts=[types.Part.from_text(text=p)])
        for item in history
        for p in item['parts']
    ]

    result=client.models.generate_content(
        model='gemini-2.0-flash',
        contents=contents
    )

    return result.text