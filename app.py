from flask import Flask,render_template,request
import api

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        prompt=request.form.get('prompt')
        response=api.response(prompt)
        return render_template('index.html',data=response)

    return render_template('index.html')