# EcoScan-AI Docker Configuration
# Build: docker build -t ecoscan-ai .
# Run: docker run -p 5000:5000 -e GEMINI_API_KEY=your_key ecoscan-ai

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000').read()"

# Set environment
ENV FLASK_APP=server.py
ENV PYTHONUNBUFFERED=1

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-t", "60", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
