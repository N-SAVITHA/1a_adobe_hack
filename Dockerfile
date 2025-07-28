FROM python:3.11-slim

# Install system dependencies for PyMuPDF and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create input and output folders
RUN mkdir -p input output

# Default command: run the pipeline
CMD ["python", "pipeline.py"]