"""Tests for the technology implementations."""

import pytest
from unittest.mock import MagicMock, patch

from core.factory import TechnologyFactory
from technologies.tesseract import TesseractTechnology
from technologies.openai import OpenAITechnology


def test_technology_registration():
    """Test that technologies are registered correctly."""
    # Reset the registry for testing
    TechnologyFactory._registry = {}
    
    # Register the technologies
    TechnologyFactory.register(TesseractTechnology)
    TechnologyFactory.register(OpenAITechnology)
    
    # Check that they are in the registry
    technologies = TechnologyFactory.list_technologies()
    assert "tesseract" in technologies
    assert "openai" in technologies
    
    # Check that we can get instances
    tesseract = TechnologyFactory.get_technology("tesseract")
    assert isinstance(tesseract, TesseractTechnology)
    
    openai = TechnologyFactory.get_technology("openai")
    assert isinstance(openai, OpenAITechnology)


@patch("technologies.tesseract.pytesseract")
@patch("technologies.tesseract.Image")
@patch("technologies.tesseract.io")
async def test_tesseract_technology(mock_io, mock_image, mock_pytesseract):
    """Test the Tesseract technology implementation."""
    # Mock the dependencies
    mock_image_instance = MagicMock()
    mock_image.open.return_value = mock_image_instance
    mock_pytesseract.image_to_string.return_value = "Test OCR result"
    
    # Create the technology
    tech = TesseractTechnology()
    
    # Run the technology
    result = await tech.run(b"test document")
    
    # Check the result
    assert result.technology_used == "tesseract"
    assert len(result.data) == 1
    assert result.data[0].text == "Test OCR result"
    
    # Check that the dependencies were called correctly
    mock_image.open.assert_called_once()
    mock_pytesseract.image_to_string.assert_called_once_with(
        mock_image_instance, lang="eng", config=""
    )


@patch("technologies.openai.openai")
@patch("technologies.openai.PyPDF2")
async def test_openai_technology(mock_pypdf2, mock_openai):
    """Test the OpenAI technology implementation."""
    # Mock the dependencies
    mock_pdf_reader = MagicMock()
    mock_pdf_reader.pages = [MagicMock(), MagicMock()]
    mock_pdf_reader.pages[0].extract_text.return_value = "Page 1 text"
    mock_pdf_reader.pages[1].extract_text.return_value = "Page 2 text"
    mock_pypdf2.PdfReader.return_value = mock_pdf_reader
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "GPT analysis result"
    mock_openai.ChatCompletion.create.return_value = mock_response
    
    # Create the technology
    tech = OpenAITechnology()
    
    # Run the technology
    result = await tech.run(
        b"test document",
        api_key="test-api-key",
        model="gpt-4"
    )
    
    # Check the result
    assert result.technology_used == "openai"
    assert len(result.data) == 1
    assert result.data[0].text == "GPT analysis result"
    
    # Check that the dependencies were called correctly
    mock_pypdf2.PdfReader.assert_called_once()
    mock_openai.ChatCompletion.create.assert_called_once()
    assert mock_openai.api_key == "test-api-key"