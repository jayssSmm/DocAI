import os
from google import genai
from dotenv import load_dotenv
load_dotenv()  # Add this before using os.getenv   

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def response(prompt):
    response=client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response