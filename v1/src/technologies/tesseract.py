"""Tesseract OCR technology implementation."""

import logging
from typing import Any, Dict, List

from core.base import BaseTechnology
from core.factory import TechnologyFactory
from core.models import DocumentChunk, ProcessingResult

logger = logging.getLogger(__name__)


class TesseractTechnology(BaseTechnology):
    """Tesseract OCR technology for extracting text from images and PDFs."""
    
    async def run(self, document: bytes, **params) -> ProcessingResult:
        """Process a document using Tesseract OCR.
        
        Args:
            document: The document content as bytes
            **params: Additional parameters for Tesseract
            
        Returns:
            ProcessingResult: The processing result
        """
        try:
            # Lazy import to avoid requiring pytesseract for all users
            import pytesseract
            from PIL import Image
            import io
            import pdf2image
            
            # Get parameters
            lang = params.get("lang", "eng")
            config = params.get("config", "")
            
            # Check if document is PDF or image
            try:
                # Try to open as image
                image = Image.open(io.BytesIO(document))
                pages = [image]
            except Exception:
                # Try to convert PDF to images
                pages = pdf2image.convert_from_bytes(document)
            
            # Process each page
            chunks: List[DocumentChunk] = []
            for i, page in enumerate(pages):
                text = pytesseract.image_to_string(page, lang=lang, config=config)
                chunks.append(DocumentChunk(
                    text=text,
                    page=i + 1,
                    metadata={"page": i + 1}
                ))
            
            # Create result
            return ProcessingResult(
                data=chunks,
                technology_used=self.get_name(),
                metadata={
                    "num_pages": len(pages),
                    "lang": lang
                }
            )
        
        except ImportError as e:
            logger.error(f"Required package not installed: {str(e)}")
            raise RuntimeError(
                f"Required package not installed: {str(e)}. "
                f"Please install pytesseract, pillow, and pdf2image."
            )
        
        except Exception as e:
            logger.error(f"Error processing document with Tesseract: {str(e)}")
            raise
    
    @classmethod
    def get_param_schema(cls) -> Dict[str, Any]:
        """Get the parameter schema for Tesseract.
        
        Returns:
            Dict[str, Any]: The parameter schema
        """
        return {
            "lang": {
                "type": "string",
                "description": "Language(s) to use for OCR",
                "default": "eng"
            },
            "config": {
                "type": "string",
                "description": "Additional Tesseract configuration",
                "default": ""
            }
        }


# Register the technology
TechnologyFactory.register(TesseractTechnology)