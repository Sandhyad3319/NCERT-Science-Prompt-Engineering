# pdf_extractor.py
import PyPDF2
import io
import requests

def extract_text_from_pdf(pdf_url):
    """
    Downloads a PDF from a given URL and extracts all text from it.

    Args:
        pdf_url (str): The URL of the PDF file.

    Returns:
        str: The extracted text from the PDF, or None if an error occurred.
    """
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        with io.BytesIO(response.content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or "" # Use .extract_text()
            return text
    except requests.exceptions.RequestException as e:
        print(f"Network or request error for {pdf_url}: {e}")
        return None
    except PyPDF2.errors.PdfReadError as e:
        print(f"PDF read error for {pdf_url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during PDF extraction from {pdf_url}: {e}")
        return None