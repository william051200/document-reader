# Document Reader API

A flexible and extensible API for processing documents using various technologies like OCR (Tesseract) and AI (OpenAI GPT).

## Features

- **Multiple Technologies**: Process documents using Tesseract OCR, OpenAI GPT, and more
- **RESTful API**: Clean API design with FastAPI
- **Extensible Architecture**: Easily add new document processing technologies
- **Containerized**: Docker and docker-compose support for easy deployment
- **Configurable**: Environment variables and configuration files

## Project Structure

```
document-reader/
├── app/            # Main application entrypoint
├── api/            # FastAPI routes and API handling
├── core/           # Core abstractions, base classes, utils
├── technologies/   # Individual technology implementations
├── config/         # Configuration management
├── tests/          # Unit & integration tests
├── outputs/        # Saved result files
```

## Installation

### Prerequisites

- Python 3.9+
- Tesseract OCR (for OCR functionality)
- Poppler (for PDF processing)

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/document-reader.git
cd document-reader

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/run.py
```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build
```

## API Usage

### Process a Document

```bash
curl -X POST "http://localhost:8000/api/v1/run" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "technology=tesseract" \
  -F "params={\"lang\":\"eng\"}"
```

### Get Processing Result

```bash
curl -X GET "http://localhost:8000/api/v1/results/{job_id}" \
  -H "accept: application/json"
```

### Check API Status

```bash
curl -X GET "http://localhost:8000/api/v1/status" \
  -H "accept: application/json"
```

## Adding a New Technology

1. Create a new file in the `technologies` directory (e.g., `technologies/new_tech.py`)
2. Implement a class that inherits from `BaseTechnology`
3. Implement the `run` method and any other required methods
4. Register the technology with `TechnologyFactory.register(NewTechnology)`

Example:

```python
from core.base import BaseTechnology
from core.factory import TechnologyFactory
from core.models import ProcessingResult

class NewTechnology(BaseTechnology):
    async def run(self, document: bytes, **params) -> ProcessingResult:
        # Process the document
        result = "Processed with new technology"
        
        # Return the result
        return ProcessingResult(
            data=result,
            technology_used=self.get_name(),
            metadata={}
        )

# Register the technology
TechnologyFactory.register(NewTechnology)
```

## Configuration

The application can be configured using environment variables:

- `API_HOST`: Host to bind the server to (default: 0.0.0.0)
- `API_PORT`: Port to bind the server to (default: 8000)
- `DEBUG`: Enable debug mode (default: false)
- `OUTPUT_DIRECTORY`: Directory to store output files

## Testing

```bash
# Run tests
pytest src/tests/
```

## Technologies

1. Landing AI - Agentic document extraction (original)
2. Tesseract OCR - Open-source OCR engine
3. OpenAI GPT - AI-powered document analysis
