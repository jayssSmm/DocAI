from flask import Blueprint,request
from app.services.llm_cache_services import redis_pdf
from app.services.pdf_services import text_based_extraction as tpdf
from app.services.llm_services import groq_provider
from app.services.session_cache_services import redis_history
from app.services.session_services import session_handler,new_session
from app.services.guest_services import too_many_request
from app.services.message_services import message_add
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request

bp=Blueprint("upload",__name__)

@bp.route('/upload',methods=['POST'])
def upload_files():
    if not request.files.get('file'):
        return {'message': 'Error: No file part'}, 400
    
    guest_id = request.headers.get("x-guest-id")
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity() 
    except Exception as e:
        print(e)
        user_id = None

    is_guest = user_id is None
    session_id = request.form.get('session_id')

    if is_guest:
        req = too_many_request.guest_limit_reached(guest_id)
        if req:
            return {
                "message": "You've reached the free limit of 5 messages. Sign up to continue.",
                 'session_id':session_id,
            }, 403
        session_id = guest_id
    
    file = request.files.get('file')

    if file.filename=='':
        return {'message': 'Error: No selected file'}, 400
        
    if file.content_type=='application/pdf':

        cache_pdf=redis_pdf.get_cache_file(file)
        if cache_pdf:
            print(session_id)
            return {'message':cache_pdf}
        else:
            r = tpdf.text_extraction(file)
            data = {"role":"user","content":r}

            if session_id=="null" and not is_guest:
                session_id = new_session.create_new_session(user_id, r)

            chat_history=session_handler.get_redis_history(session_id,is_guest,data)
            
            pdf_response=groq_provider.response(r,chat_history)
 
                
            redis_pdf.set_cache_file(file,pdf_response)
            redis_history.set_history(session_id,"user",r)
            redis_history.set_history(session_id,"assistant",pdf_response)

            if not is_guest:
                message_add.add_message(session_id,'user',r)
                message_add.add_message(session_id,'assistant',pdf_response)

            return {'message':pdf_response, "session_id":session_id}
        
    return {'message':'Error: Upload pdf Only'} , 400