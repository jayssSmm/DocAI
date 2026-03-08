import os
from google import genai

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def response(prompt):
    result=client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return result