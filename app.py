from flask import Flask,render_template,request,session,redirect
from api import groq_provider
from api import gemini_provider

app=Flask(__name__)
app.secret_key = "new2_random_string_here"

@app.route('/', methods=['GET','POST'])
def index():

    if 'chat_history_groq' not in session:
        session['chat_history_groq']=[]

    if 'chat_history_gemini' not in session:
        session['chat_history_gemini']=[]

    if request.method=='POST':
        prompt=request.form.get('prompt')
        model=request.form.get('model')
        try:
            if model=='Groq':
                response=groq_provider.response(prompt,session['chat_history_groq'])
                session['chat_history_groq'].append({'role':'assistant','content':response})
            else:
                response=gemini_provider.response(prompt,session['chat_history_gemini'])
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