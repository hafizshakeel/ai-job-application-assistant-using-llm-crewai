"""
PDF Processing utility for the Job Application Assistant
"""
import os
import io
import logging
from typing import Optional, BinaryIO

# Importing PyPDF2 for PDF processing
try:
    from PyPDF2 import PdfReader
except ImportError:
    # Provide helpful error message if PyPDF2 is not installed
    raise ImportError(
        "PyPDF2 is required for PDF processing. Please install it using: pip install PyPDF2"
    )

# Configure logging
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Utility for processing PDF resume files"""
    
    @staticmethod
    def extract_text_from_pdf(file: BinaryIO) -> Optional[str]:
        """
        Extract text content from a PDF file
        
        Args:
            file: PDF file object (file upload from Streamlit)
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            # Read the PDF file
            pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
            
            # Extract text from each page
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return None