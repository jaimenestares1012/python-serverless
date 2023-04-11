import base64
import io
import json
import re
# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer
from pdfminer.converter import HTMLConverter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from bs4 import BeautifulSoup


import mysql.connector
# def extract_pdf_text(base64_pdf):
#     pdf_bytes = base64.b64decode(base64_pdf)
#     pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
#     html_pages = []

#     for page in pdf_document:
#         html = page.get_text("html")
#         html_pages.append(html)

#     return "".join(html_pages)


def extract_pdf_text(base64_pdf):
    pdf_bytes = base64.b64decode(base64_pdf)
    rsrcmgr = PDFResourceManager()
    retstr = io.BytesIO()
    device = HTMLConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(io.BytesIO(pdf_bytes)):
        interpreter.process_page(page)

    html_bytes = retstr.getvalue()
    html_string = html_bytes.decode('utf-8')
    device.close()
    retstr.close()
    return html_string



# import json
# import base64
# import io
# from PyPDF2 import PdfReader
# import pikepdf
# import re
# from pdfminer.high_level import extract_text 


# def extract_pdf_text(base64_pdf):
#     pdf_bytes = base64.b64decode(base64_pdf)
#     pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
#     text = ""
#     pdf_reader.pages[0].extract_text()
#     # for page in pdf_reader.pages:
#     #     text += page.extract_text()
#     return pdf_reader.pages[0].extract_text()

# def extract_pdf_text(base64_pdf):
#     pdf_bytes = base64.b64decode(base64_pdf)
#     text = extract_text(io.BytesIO(pdf_bytes))
#     return text


def clean_text(text):
    # Eliminar caracteres de retorno de carro y saltos de línea
    text = re.sub(r'\n|\r', '', text)
    
    # Eliminar caracteres no imprimibles
    text = re.sub(r'[^\x20-\x7E]', '', text)
    
    # # Eliminar caracteres no alfabéticos o numéricos
    text = re.sub(r'[^\w\s]', '', text)

    
    # # Eliminar espacios en blanco adicionales
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def handler(event, context):
    body = json.loads(event["body"])
    base64_pdf = body["base64"]
    identificador = body["identificador"]
    text = extract_pdf_text(base64_pdf)
    soup = BeautifulSoup(text, 'html.parser')
    element = soup.find('div', {'style': 'position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:526px; top:436px; width:47px; height:9px;'}).text.strip()
    num = int(element.rstrip('.').replace(',', ''))


    div = soup.find('div', {'style': 'position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:427px; top:599px; width:41px; height:9px;'})    
    valor = div.find('span').text.strip()
    deductions = int(valor.rstrip('.').replace(',', ''))


    cnx = mysql.connector.connect(user='admin', password='12345678', host='database-prueba-tecnica.c0ffrigz07gs.us-east-1.rds.amazonaws.com', database='test')
    cursor = cnx.cursor()
    add_data = ("UPDATE registros SET tax_filing = %s, wages = %s, total_deductions = %s WHERE id = %s")
    data_values = ('Nodata', num, deductions, identificador)
    cursor.execute(add_data, data_values)
    query = "SELECT * FROM registros WHERE id = {}".format(identificador)
    print("query", query)
    cursor.execute(query)
    rows = cursor.fetchall()[0]
    keys = ('id', 'nombre', 'apellido', 'correo', 'tax_filing', 'wages', 'total_deductions')

    registro = {}
    for i in range(len(keys)):
        registro[keys[i]] = rows[i]

    json_registro = json.dumps(registro)
    print(json_registro)
    print("<------------------------------------------->")




    cnx.commit()
    cursor.close()
    cnx.close()
    

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
        },
        "body": json.dumps(registro)
    }
    return response


    # print("base type", type(base))
    # pdf_bytes = base64.b64decode(base)
    # pdf_stream = BytesIO(pdf_bytes)
    
    # with pikepdf.open(pdf_stream) as pdf:
    #     print(f"El archivo tiene {len(pdf.pages)} páginas.")
    #     # Extraer el texto de la primera página
    #     page = pdf.pages[0]
    #     text = page.extract_text()
    #     print(text)

    # response = {
    #     "statusCode": 200,
    #     "body": ""
    # }


# import base64
# import io
# import os
# import json
# import pdfminer.high_level
# from bs4 import BeautifulSoup
# import subprocess
# def handler(event, context):
#     body = json.loads(event["body"])
#     # Decodificar el archivo PDF en base64
#     base64_pdf = body["base64"]
#     pdf_bytes = base64.b64decode(base64_pdf)
#     output_string = io.StringIO()
#     pdfminer.high_level.extract_text(io.BytesIO(pdf_bytes), output_type='html', codec='utf-8', laparams=None, maxpages=0, caching=True, password='', check_extractable=True).write_html(output_string)

#     soup = BeautifulSoup(output_string.getvalue(), 'html.parser')
#     return soup.prettify()