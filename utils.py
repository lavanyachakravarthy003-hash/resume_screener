import fitz  # PyMuPDF

def read_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    
    for page in doc:
        text += page.get_text()
    
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])