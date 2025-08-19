# Multi-stage build for Document Reader API

# Stage 1: Build dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Install additional dependencies for Tesseract
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels \
    pytesseract \
    pdf2image \
    Pillow \
    PyPDF2 \
    openai \
    fastapi \
    uvicorn[standard] \
    python-multipart \
    pytest \
    pytest-asyncio

# Stage 2: Runtime image
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY src/ /app/src/
COPY requirements.txt /app/

# Create output directory
RUN mkdir -p /app/outputs

# Set environment variables
ENV PYTHONPATH=/app
ENV OUTPUT_DIRECTORY=/app/outputs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "/app/src/run.py"]