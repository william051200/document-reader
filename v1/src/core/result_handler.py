"""Result handler for saving and retrieving processing results."""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from config.settings import settings
from core.models import ProcessRequest, ProcessingResult, ResultResponse

logger = logging.getLogger(__name__)


class ResultHandler:
    """Handler for saving and retrieving processing results."""
    
    def __init__(self):
        """Initialize the result handler."""
        self.output_dir = Path(settings.output_directory)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_result(self, result: ProcessingResult, request: ProcessRequest) -> str:
        """Save a processing result.
        
        Args:
            result: The processing result
            request: The original request
            
        Returns:
            str: The job ID
        """
        # Generate a unique job ID
        job_id = str(uuid.uuid4())
        
        # Create result directory
        result_dir = self.output_dir / job_id
        result_dir.mkdir(parents=True, exist_ok=True)
        
        # Save result as JSON
        result_path = result_dir / "result.json"
        with open(result_path, "w") as f:
            json.dump(result.dict(), f, default=self._json_serializer)
        
        # Save request for reference
        request_path = result_dir / "request.json"
        with open(request_path, "w") as f:
            json.dump(request.dict(), f)
        
        # Save markdown output
        markdown_path = result_dir / "output.md"
        with open(markdown_path, "w") as f:
            f.write(result.markdown)
        
        logger.info(f"Saved result {job_id} to {result_dir}")
        return job_id
    
    def get_result(self, job_id: str) -> Optional[ResultResponse]:
        """Get a processing result by job ID.
        
        Args:
            job_id: The job ID
            
        Returns:
            Optional[ResultResponse]: The result response, or None if not found
        """
        result_dir = self.output_dir / job_id
        result_path = result_dir / "result.json"
        
        if not result_path.exists():
            logger.warning(f"Result {job_id} not found")
            return None
        
        try:
            with open(result_path, "r") as f:
                result_data = json.load(f)
            
            # Convert datetime strings back to datetime objects
            if "processed_at" in result_data and isinstance(result_data["processed_at"], str):
                result_data["processed_at"] = datetime.fromisoformat(result_data["processed_at"])
            
            result = ProcessingResult(**result_data)
            
            return ResultResponse(
                job_id=job_id,
                result=result,
                status="completed"
            )
        
        except Exception as e:
            logger.error(f"Error loading result {job_id}: {str(e)}")
            return None
    
    @staticmethod
    def _json_serializer(obj):
        """Custom JSON serializer for objects not serializable by default json code.
        
        Args:
            obj: The object to serialize
            
        Returns:
            str: The serialized object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        
        raise TypeError(f"Type {type(obj)} not serializable")