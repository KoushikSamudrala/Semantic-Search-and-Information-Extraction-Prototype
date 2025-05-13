import io
from tika import parser

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Parse PDF bytes using Apache Tika and return extracted plain text.
    """
    parsed = parser.from_buffer(pdf_bytes)
    return parsed.get('content', '')