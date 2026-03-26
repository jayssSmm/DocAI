import pymupdf
import pathlib
import dotenv
import os

dotenv.load_dotenv(override=True)

def text_extraction(file):
    file.seek(0)          # reset pointer (important)
    pdf_bytes = file.read()

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    text = ''
    for page in doc:
        text += page.get_text('text') + '\n'

    doc.close()
    return text

if __name__=='__main__':
    path=pathlib.Path(os.getenv('FILE_PATH'))
    if not path.exists():
        print(f"Still can't find it. I'm looking at: {path.resolve()}")
    else:
        print(text_extraction(path))
