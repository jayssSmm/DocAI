from flask import Flask,render_template,request,redirect
from api import groq_provider
import redis

app=Flask(__name__)
app.secret_key = "new2_random_string_here"

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

n_groq=1

@app.route('/', methods=['GET','POST'])
def index():
    global n_groq

    if request.method=='POST':

        prompt=request.form.get('prompt')
        model=request.form.get('model')

        cache_key_groq=[r.hgetall(i) for i in r.lrange('cache_groq',0,-1)]
        cache_groq=list(filter(lambda x:x['prompt']==prompt,cache_key_groq))

        try:
            if model=='Groq':
                if cache_groq:
                    response=cache_groq[0]['content']
                else:
                    chat_history=[
                        {k:v for k,v in r.hgetall(i).items() if k in ['role','content']}
                        for i in r.lrange('chat_history_groq',0,-1)
                        ]
                    response=groq_provider.response(prompt,chat_history)
                    
                    r.hset(f'message:{n_groq}',mapping={'role':'assistant','content':response,'prompt':prompt})
                    r.expire(f'message:{n_groq}',300)
                    r.lpush('chat_history_groq',f'message:{n_groq}')
                    n_groq+=1

            return render_template('index.html',data=response)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', data="Sorry, the AI is having trouble right now.")

    return render_template('index.html')

@app.route('/clear')
def clear():
    global n_groq
    n_groq=1
    r.flushall()
    return redirect('/')

@app.roue('/upload')
def upload_files():
