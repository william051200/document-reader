# Agentic Document Extraction App

## Overview
This application provides a unified interface to process documents using multiple technologies (e.g., Agentic Document Extraction, Textract, Tesseract, etc.).  
It exposes APIs for other applications to interact with, and supports saving extracted data to files.  

The architecture emphasizes:
- Maintainability (easily add/remove technologies)
- Scalability (supports multiple backends)
- Clean separation of concerns (OOP + design patterns)

---

## Project Structure
```
agentic_doc_extraction_app/
│
├── api/                    # Flask/FastAPI endpoints
│   └── routes.py           # Defines API routes and request handling
│
├── core/                   # Core interfaces, base classes, and orchestration
│   ├── base_technology.py  # Abstract base class for all technologies
│   ├── manager.py          # Chooses and runs the appropriate technology
│   └── config.py           # Global configuration loader
│
├── technologies/           # Implementations of various extraction technologies
│   ├── agentic_extraction.py   # Example: Agentic Document Extraction
│   ├── textract_extraction.py  # Example: AWS Textract wrapper
│   └── tesseract_extraction.py # Example: Tesseract OCR wrapper
│
├── utils/                  # Utility modules (logging, file saving, etc.)
│   ├── file_handler.py
│   └── logger.py
│
├── main.py                 # App entry point (runs API server)
├── requirements.txt        # Dependencies list
└── config.yaml             # Configurable parameters (technologies, file paths, API settings)
```

---

## Setup Instructions

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure application
Edit `config.yaml` to specify:
- Default technology
- Parameters for each technology
- File output paths
- API server settings

### 4. Run application
```bash
python main.py
```

---

## Extending the Application

1. Create a new file in `technologies/` (e.g., `new_tech_extraction.py`).  
2. Implement a class that inherits from `BaseTechnology` in `core/base_technology.py`.  
3. Add any specific parameters to `config.yaml`.  
4. Register the technology in `core/manager.py`.  

Example stub:
```python
from core.base_technology import BaseTechnology

class NewTechExtraction(BaseTechnology):
    def __init__(self, config):
        super().__init__(config)

    def run(self, image):
        # implement document extraction logic here
        return extracted_data
```

---

## API Example

`POST /extract`  
Request:
```json
{
  "technology": "agentic",
  "image_path": "path/to/document.png",
  "params": {"api_key": "12345"}
}
```

Response:
```json
{
  "status": "success",
  "data": { "field1": "value1", "field2": "value2" }
}
```

---

## Next Steps
- Define detailed schemas for input/output in API
- Add authentication/authorization if needed
- Implement async job handling for long-running extractions
