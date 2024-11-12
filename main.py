from fasthtml.common import *
from CreateBill import CreateBill
import os

app = FastHTML(hdrs=(
    Link(rel="stylesheet", href="output.css", type="text/css")
))

upload_dir = Path("media")
upload_dir.mkdir(exist_ok=True)

@app.route("/{fname:path}.{ext:static}")
def get(fname:str, ext:str): 
    return FileResponse(f'static/{fname}.{ext}')

@app.route('/')
def get():
    return Div(
        H1("Grameen Media"),
        Form(
            Input(type='text', name='bill_no', placeholder='Enter Bill Number'),
            Input(type='text', name='brand', placeholder='Brand'),
            Input(type='text', name='showroom', placeholder='Showroom'),
            Input(type='text', name='address', placeholder='Address'),
            Input(type='text', name='mobile', placeholder='Mobile'),
            Textarea(type='text', name='board', placeholder='Specification of Boards'),
            Input(type='submit', name='submit', value='Submit'),
            action='/create',
            method='post',
            hx_on='htmx:afterRequest:this.reset()'
        ),
        Div(id='thanks')
    )

@app.route("/create")
def post(bill_no:str, brand:str, showroom:str, address:str, mobile:str, board:str):
    file_path = os.path.join(upload_dir, f'{bill_no} {showroom}.docx') 
    CreateBill(bill_no, brand, showroom, address, mobile, board, file_path)

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path, 
            filename=f'{bill_no} {showroom}.docx',
            media_type="application/octet-stream"
        )
    else:
        return P('Sorry mission failed')

serve()