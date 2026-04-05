from flask import Blueprint,request
from app.services.llm_cache_services import redis_pdf
from app.services.pdf_services import text_based_extraction as tpdf
from app.services.llm_services import groq_provider
from app.services.session_cache_services import redis_history

bp=Blueprint("upload",__name__)

@bp.route('/upload',methods=['POST'])
def upload_files():
    if not request.files.get('file'):
        return {'message': 'Error: No file part'}, 400
    
    file = request.files.get('file')

    if file.filename=='':
        return {'message': 'Error: No selected file'}, 400
        
    if file.content_type=='application/pdf':

        cache_pdf=redis_pdf.get_cache_file(file)
        if cache_pdf:
            return {'message':cache_pdf}
        else:
            chat_history=redis_history.get_last_ten_messages()

            r = tpdf.text_extraction(file)
            pdf_response=groq_provider.response(r,chat_history)
                
            redis_pdf.set_cache_file(file,pdf_response)
            redis_history.set_history(pdf_response)

            return {'message':pdf_response}
        
    return {'message':'Error: Upload pdf Only'} , 400