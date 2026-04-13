from flask import Blueprint,request
from app.services.llm_cache_services import redis_pdf
from app.services.pdf_services import text_based_extraction as tpdf
from app.services.llm_services import groq_provider
from app.services.session_cache_services import redis_history
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request
import json

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
    
    file = request.files.get('file')
    session_id = json.loads(session_id)

    if file.filename=='':
        return {'message': 'Error: No selected file'}, 400
        
    if file.content_type=='application/pdf':

        cache_pdf=redis_pdf.get_cache_file(file)
        if cache_pdf:
            return {'message':cache_pdf}
        else:
            chat_history=redis_history.get_last_ten_messages(session_id)

            r = tpdf.text_extraction(file)
            pdf_response=groq_provider.response(r,chat_history)
                
            redis_pdf.set_cache_file(file,pdf_response)
            redis_history.set_history(pdf_response)

            return {'message':pdf_response}
        
    return {'message':'Error: Upload pdf Only'} , 400