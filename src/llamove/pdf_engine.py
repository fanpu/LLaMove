import PyPDF2

class PDFEngine:
    
    def __init__(self):
        pass
        
    def extract_contents(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)


            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text

pdf_path = '../../tests/sample_pdfs/attention.pdf'

engine = PDFEngine()
text = engine.extract_contents(pdf_path)

with open("output.txt", "w") as f:
    f.write(text)