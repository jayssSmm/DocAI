from flask import Flask,render_template,request,session,redirect
from api import groq_provider
from api import gemini_provider
import redis

app=Flask(__name__)
app.secret_key = "new2_random_string_here"

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

@app.route('/', methods=['GET','POST'])
def index():

    if 'chat_history_groq' not in session:
        session['chat_history_groq']=[]

    if 'chat_history_gemini' not in session:
        session['chat_history_gemini']=[]

    if request.method=='POST':
        prompt=request.form.get('prompt')
        model=request.form.get('model')

        cache=r.get(prompt)

        try:
            if model=='Groq':
                if cache:
                    response=cache
                else:
                    response=groq_provider.response(prompt,session['chat_history_groq'])
                    r.set(prompt,response,ex=300)
                    session['chat_history_groq'].append({'role':'assistant','content':response})
                    
            elif model=='Gemini':
                if cache:
                    response=cache
                else:
                    response=gemini_provider.response(prompt,session['chat_history_gemini'])
                    r.set(prompt,response,ex=300)
                    session['chat_history_gemini'].append({'role':'model','parts':[response]})

            session.modified=True

            return render_template('index.html',data=response)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', data="Sorry, the AI is having trouble right now.")

    return render_template('index.html')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')