"""API router for document processing endpoints."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import ValidationError

from core.factory import TechnologyFactory
from core.models import ProcessRequest, ProcessResponse, ResultResponse
from core.result_handler import ResultHandler

api_router = APIRouter()


@api_router.post("/run", response_model=ProcessResponse, status_code=status.HTTP_202_ACCEPTED)
async def run_document_processing(
    file: UploadFile = File(...),
    technology: str = Form(...),
    params: str = Form("{}")
):
    """Process a document using the specified technology.
    
    Args:
        file: The document file to process
        technology: The technology to use for processing
        params: JSON string of parameters for the technology
        
    Returns:
        ProcessResponse: Response with job ID
    """
    try:
        # Parse request
        request = ProcessRequest(
            technology=technology,
            params=params,
            filename=file.filename
        )
        
        # Get technology implementation
        tech_impl = TechnologyFactory.get_technology(request.technology)
        
        # Process the document
        contents = await file.read()
        result = await tech_impl.run(contents, **request.params_dict)
        
        # Save result
        result_handler = ResultHandler()
        job_id = result_handler.save_result(result, request)
        
        return ProcessResponse(job_id=job_id, status="processing")
    
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request parameters: {str(e)}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown technology: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )


@api_router.get("/results/{job_id}", response_model=ResultResponse)
async def get_result(job_id: str):
    """Get the result of a document processing job.
    
    Args:
        job_id: The ID of the job
        
    Returns:
        ResultResponse: The result of the job
    """
    try:
        result_handler = ResultHandler()
        result = result_handler.get_result(job_id)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Result with ID {job_id} not found"
            )
        
        return result
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving result: {str(e)}"
        )


@api_router.get("/status")
async def get_status():
    """Get the status of the API."""
    return {"status": "running"}


@api_router.post("/config")
async def update_config():
    """Update the configuration dynamically.
    
    This is a placeholder for future implementation.
    """
    return {"status": "not implemented"}