from flask import Flask,render_template,request
from api import groq_provider

app=Flask(__name__)

message=[]

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':

        prompt=request.form.get('prompt')
        response=groq_provider.response(prompt,message)

        message.append({'role':'assistant','content':response})

        return render_template('index.html',data=response)

    return render_template('index.html')