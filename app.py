from flask import Flask,render_template,request,session
from api import groq_provider

app=Flask(__name__)
app.secret_key = "any_random_string_here"

@app.route('/', methods=['GET','POST'])
def index():

    if 'chat_history' not in session:
        session['chat_history']=[]

    if request.method=='POST':
        prompt=request.form.get('prompt')
        try:
            response=groq_provider.response(prompt,session['chat_history'])
            session['chat_history'].append({'role':'assistant','content':response})
            session.modified=True
            return render_template('index.html',data=response)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', data="Sorry, the AI is having trouble right now.")

    return render_template('index.html')