# backend/file_utils.py
import os
import tempfile
import PyPDF2

def save_uploaded_file(file):
    """Saves an uploaded file to a temporary location."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    file.save(temp_file.name)
    return temp_file.name

def read_file(filepath):
    """Reads a text file or PDF and returns its content."""
    try:
        if filepath.lower().endswith('.pdf'):
            return read_pdf(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
    except FileNotFoundError:
        return ""

def read_pdf(filepath):
    """Reads a PDF file and returns its text content."""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def delete_file(filepath):
    """Deletes a file."""
    try:
        os.remove(filepath)
    except OSError:
        pass