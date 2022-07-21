import PyPDF2 as pypdf
from PyPDF2.generic import NameObject, BooleanObject,IndirectObject
# ========= Global defined variables =============
FilePath = "Interactive_form.pdf"

def Main(FilePath):
    try:
        with open(FilePath, 'rb') as f:
            reader = pypdf.PdfFileReader(f)
            firstPage = reader.getFormTextFields()
            print(firstPage)
    except Exception as e:
        print(f'Main Error Thrown: {e}')

Main(FilePath)



    

    
        
