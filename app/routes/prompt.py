from flask import Blueprint,request
from app.services.llm_cache_services import redis_text
from app.services.session_cache_services import redis_history
from app.services.yt_services import transcript_extractor
from app.services.llm_services import groq_provider
from app.services.session_services import new_session
from app.services.message_services import message_add
from app.services.guest_services import too_many_request
from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request

bp=Blueprint('prompt',__name__)

@bp.route('/prompt', methods=['POST'])
def prompt():

    data = request.get_json(silent=True)

    if not data:
        print("NO JSON RECEIVED")
        return {'message': 'No JSON received'}, 400

    prompt=data.get('prompt')
    model=data.get('model')
    session_id=data.get('session_id')

    cache_groq=redis_text.get_cached_response(prompt)

    guest_id = request.headers.get("x-guest-id")
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity() 
    except Exception as e:
        print(e)
        user_id = None

    is_guest = user_id is None

    try:
        if model == 'Groq':

            if is_guest:
                req = too_many_request.guest_limit_reached(guest_id)
                if req:
                    return {
                        "message": "You've reached the free limit of 5 messages. Sign up to continue.",
                        'session_id':session_id,
                    }, 403
                session_id = guest_id

            if not session_id and not is_guest:
                session_id = new_session.create_new_session(user_id, prompt)

            chat_history=redis_history.get_last_ten_messages(session_id)

            if not chat_history and not is_guest:
                session_history = message_add.get_message(session_id)
                for data in session_history:
                    redis_history.set_history(session_id,data['role'],data['content'])
                chat_history = redis_history.get_last_ten_messages(session_id)

            if cache_groq:
                response=cache_groq

            elif "youtube.com/watch" in prompt or "youtu.be/" in prompt:
                transcript = transcript_extractor.get_transcript(prompt)
                response = groq_provider.response(transcript,chat_history)
            else:
                response=groq_provider.response(prompt,chat_history)
            
            #code below handles cache
            redis_text.set_cached_response(prompt,response) 

            redis_history.set_history(session_id,'user',prompt)
            redis_history.set_history(session_id,'assistant',response)   
            
            #code below handles messages to db
            if not is_guest:
                message_add.add_message(session_id,'user',prompt)
                message_add.add_message(session_id,'assistant',response)

            return {'message':response, 'session_id':session_id}

        return {'message': 'Invalid model selected'}
    
    except Exception as e:
        print(f"Error: {e}")
        return {'message': "Sorry, the AI is having trouble right now."}