"""Tests for the API endpoints."""

import io
import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from core.models import ProcessingResult


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_api_status(client):
    """Test the API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}


@patch("core.factory.TechnologyFactory.get_technology")
@patch("core.result_handler.ResultHandler.save_result")
async def test_run_document_processing(mock_save_result, mock_get_technology, client):
    """Test the document processing endpoint."""
    # Mock the technology implementation
    mock_tech = MagicMock()
    mock_tech.run.return_value = ProcessingResult(
        data="Test result",
        technology_used="test_tech",
        metadata={}
    )
    mock_get_technology.return_value = mock_tech
    
    # Mock the result handler
    mock_save_result.return_value = "test-job-id"
    
    # Create a test file
    test_file = io.BytesIO(b"test content")
    test_file.name = "test.pdf"
    
    # Make the request
    response = client.post(
        "/api/v1/run",
        files={"file": ("test.pdf", test_file, "application/pdf")},
        data={
            "technology": "test_tech",
            "params": json.dumps({"param1": "value1"})
        }
    )
    
    # Check the response
    assert response.status_code == 202
    assert response.json() == {
        "job_id": "test-job-id",
        "status": "processing"
    }
    
    # Check that the technology was called correctly
    mock_get_technology.assert_called_once_with("test_tech")
    mock_tech.run.assert_called_once()
    mock_save_result.assert_called_once()


@patch("core.result_handler.ResultHandler.get_result")
async def test_get_result(mock_get_result, client):
    """Test the result retrieval endpoint."""
    # Mock the result handler
    mock_get_result.return_value = {
        "job_id": "test-job-id",
        "result": {
            "data": "Test result",
            "technology_used": "test_tech",
            "metadata": {}
        },
        "status": "completed"
    }
    
    # Make the request
    response = client.get("/api/v1/results/test-job-id")
    
    # Check the response
    assert response.status_code == 200
    assert response.json()["job_id"] == "test-job-id"
    assert response.json()["status"] == "completed"
    
    # Check that the result handler was called correctly
    mock_get_result.assert_called_once_with("test-job-id")