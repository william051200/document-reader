"""OpenAI technology implementation for document processing."""

import logging
from typing import Any, Dict, List

from core.base import BaseTechnology
from core.factory import TechnologyFactory
from core.models import DocumentChunk, ProcessingResult

logger = logging.getLogger(__name__)


class OpenAITechnology(BaseTechnology):
    """OpenAI technology for processing documents using GPT models."""
    
    async def run(self, document: bytes, **params) -> ProcessingResult:
        """Process a document using OpenAI's GPT models.
        
        Args:
            document: The document content as bytes
            **params: Additional parameters for OpenAI
            
        Returns:
            ProcessingResult: The processing result
        """
        try:
            # Lazy import to avoid requiring openai for all users
            import openai
            import io
            import PyPDF2
            
            # Get parameters
            model = params.get("model", "gpt-4")
            api_key = params.get("api_key")
            max_tokens = params.get("max_tokens", 1000)
            temperature = params.get("temperature", 0.0)
            prompt_template = params.get(
                "prompt_template",
                "Extract the key information from this document:\n\n{text}"
            )
            
            if not api_key:
                raise ValueError("OpenAI API key is required")
            
            # Set API key
            openai.api_key = api_key
            
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(document))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            
            # Prepare chunks for processing
            chunks: List[DocumentChunk] = []
            
            # Process with OpenAI
            prompt = prompt_template.format(text=text)
            
            # Use the appropriate API based on the model
            if model.startswith("gpt-4") or model.startswith("gpt-3.5"):
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a document analysis assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                result_text = response.choices[0].message.content
            else:
                response = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                result_text = response.choices[0].text
            
            # Create a single chunk with the result
            chunks.append(DocumentChunk(
                text=result_text,
                metadata={"model": model}
            ))
            
            # Create result
            return ProcessingResult(
                data=chunks,
                technology_used=self.get_name(),
                metadata={
                    "model": model,
                    "num_pages": len(pdf_reader.pages)
                }
            )
        
        except ImportError as e:
            logger.error(f"Required package not installed: {str(e)}")
            raise RuntimeError(
                f"Required package not installed: {str(e)}. "
                f"Please install openai and PyPDF2."
            )
        
        except Exception as e:
            logger.error(f"Error processing document with OpenAI: {str(e)}")
            raise
    
    @classmethod
    def get_param_schema(cls) -> Dict[str, Any]:
        """Get the parameter schema for OpenAI.
        
        Returns:
            Dict[str, Any]: The parameter schema
        """
        return {
            "api_key": {
                "type": "string",
                "description": "OpenAI API key",
                "required": True
            },
            "model": {
                "type": "string",
                "description": "OpenAI model to use",
                "default": "gpt-4",
                "enum": ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
            },
            "max_tokens": {
                "type": "integer",
                "description": "Maximum tokens in the response",
                "default": 1000
            },
            "temperature": {
                "type": "number",
                "description": "Sampling temperature",
                "default": 0.0,
                "minimum": 0.0,
                "maximum": 2.0
            },
            "prompt_template": {
                "type": "string",
                "description": "Template for the prompt, use {text} as placeholder for document text",
                "default": "Extract the key information from this document:\n\n{text}"
            }
        }


# Register the technology
TechnologyFactory.register(OpenAITechnology)