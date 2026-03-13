from flask import Flask,render_template,request,redirect
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

n_groq=1
n_gemini=1

@app.route('/', methods=['GET','POST'])
def index():
    global n_groq
    global n_gemini

    if request.method=='POST':

        prompt=request.form.get('prompt')
        model=request.form.get('model')

        cache_key_groq=[r.hgetall(i) for i in r.lrange('chat_history_groq',0,-1)]
        cache_groq=list(filter(lambda x:x['prompt']==prompt,cache_key_groq))
                        
        cache_key_gemini=[i for i in r.lrange('chat_history_gemini',0,-1)]
        cache_gemini=filter(lambda x:x['prompt']==prompt,cache_key_gemini)

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
                    r.lpush('chat_history_groq',f'message:{n_groq}')

                    n_groq+=1
                    
            elif model=='Gemini':
                if cache_gemini:
                    response=cache_gemini[0]['parts']
                else:
                    chat_history=[
                        {k:v for k,v in i.hgetall().items() if k in ['role','parts']}
                        for i in r.lrange('chat_history_gemini',0,-1)
                    ]
                    response=gemini_provider.response(prompt,chat_history)

                    r.hset(f'message:{n_gemini}',mapping={'role':'model','parts':[response],'prompt':prompt})
                    r.expire(300)
                    r.lpush('chat_history_gemini',f'message:{n_gemini}')

                    n_gemini+=1

            return render_template('index.html',data=response)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', data="Sorry, the AI is having trouble right now.")

    return render_template('index.html')

@app.route('/clear')
def clear():
    r.flushall()
    return redirect('/')