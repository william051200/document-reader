"""Data models for the application."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class ProcessRequest(BaseModel):
    """Request model for document processing."""
    technology: str
    params: str = "{}"
    filename: str
    
    @property
    def params_dict(self) -> Dict[str, Any]:
        """Get the parameters as a dictionary.
        
        Returns:
            Dict[str, Any]: The parameters as a dictionary
        """
        if not self.params:
            return {}
        return json.loads(self.params)


class ProcessResponse(BaseModel):
    """Response model for document processing."""
    job_id: str
    status: str


class DocumentChunk(BaseModel):
    """Model for a chunk of document content."""
    text: str
    page: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProcessingResult(BaseModel):
    """Model for document processing result."""
    data: Union[str, List[DocumentChunk]]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    technology_used: str
    processed_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def markdown(self) -> str:
        """Get the result as markdown.
        
        Returns:
            str: The result as markdown
        """
        if isinstance(self.data, str):
            return self.data
        
        # Convert chunks to markdown
        result = ""
        for chunk in self.data:
            if chunk.page is not None:
                result += f"## Page {chunk.page}\n\n"
            result += f"{chunk.text}\n\n"
        
        return result
    
    @property
    def chunks(self) -> List[Dict[str, Any]]:
        """Get the result as chunks.
        
        Returns:
            List[Dict[str, Any]]: The result as chunks
        """
        if isinstance(self.data, str):
            # Convert markdown to a single chunk
            return [{
                "text": self.data,
                "metadata": self.metadata
            }]
        
        return [chunk.dict() for chunk in self.data]


class ResultResponse(BaseModel):
    """Response model for result retrieval."""
    job_id: str
    result: ProcessingResult
    status: str = "completed"