"""Base technology abstract class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Union


class BaseTechnology(ABC):
    """Base class for all document processing technologies.
    
    All technology implementations must inherit from this class and implement
    the required methods.
    """
    
    @abstractmethod
    async def run(self, document: bytes, **params) -> Dict[str, Any]:
        """Process a document using this technology.
        
        Args:
            document: The document content as bytes
            **params: Additional parameters for the technology
            
        Returns:
            Dict[str, Any]: The processing result
        """
        pass
    
    @classmethod
    def get_name(cls) -> str:
        """Get the name of the technology.
        
        Returns:
            str: The name of the technology
        """
        return cls.__name__.lower().replace('technology', '')
    
    @classmethod
    def get_description(cls) -> str:
        """Get the description of the technology.
        
        Returns:
            str: The description of the technology
        """
        return cls.__doc__ or "No description available"
    
    @classmethod
    def get_param_schema(cls) -> Dict[str, Any]:
        """Get the parameter schema for the technology.
        
        Returns:
            Dict[str, Any]: The parameter schema
        """
        return {}