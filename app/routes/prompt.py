from flask import Blueprint,request
from app.services.llm_cache_services import redis_text
from app.services.session_cache_services import redis_history
from app.services.yt_services import transcript_extractor
from app.services.llm_services import groq_provider
from app.services.session_services import new_session
from app.services.message_services import message_add
from flask_jwt_extended import jwt_required,get_jwt_identity

bp=Blueprint('prompt',__name__)

@bp.route('/prompt', methods=['POST'])
@jwt_required()
def prompt():

    data = request.get_json(silent=True)

    if not data:
        print("NO JSON RECEIVED")
        return {'message': 'No JSON received'}, 400

    prompt=data.get('prompt')
    model=data.get('model')
    session_id=data.get('session_id')

    cache_groq=redis_text.get_cached_response(prompt)
    user_id=get_jwt_identity()

    try:
        if model == 'Groq':

            if not session_id:
                session_id=new_session.create_new_session(user_id,prompt)

            chat_history=redis_history.get_last_ten_messages()

            if "youtube.com/watch" in prompt or "youtu.be/" in prompt:
                if cache_groq:
                    response=cache_groq
                else:
                    transcript = transcript_extractor.get_transcript(prompt)
                    response = groq_provider.response(transcript,chat_history)
            else:
                if cache_groq:
                    response=cache_groq
                else:
                    response=groq_provider.response(prompt,chat_history)
            
            #code below handles cache
            redis_text.set_cached_response(prompt,response) 
            redis_history.set_history(response)   
            
            #code below handles messages to db
            message_add.add_message(session_id,'user',prompt)
            message_add.add_message(session_id,'assistant',response)
                
            return {'message':response, 'session_id':session_id}

        return {'message': 'Invalid model selected'}
    
    except Exception as e:
        print(f"Error: {e}")
        return {'message': "Sorry, the AI is having trouble right now."}