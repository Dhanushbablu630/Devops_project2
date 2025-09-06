# Use official Python runtime as base image
FROM python:3.9-slim

# Set environment variables (to prevent Python from buffering stdout/stderr)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Flask app port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
