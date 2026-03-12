import os
from openai import OpenAI

client=OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv('GROQ_API_KEY')
)

def response(prompt,chat_history):
    try:
        chat_history.append({'role':'user','content':prompt})
        result=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
        )
        return result.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"