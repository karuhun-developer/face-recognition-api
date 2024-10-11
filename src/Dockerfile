FROM python:3.10.12-slim

# Set work directory
WORKDIR /usr/app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake libssl-dev libffi-dev libpq-dev pkg-config libxml2-dev libxmlsec1-dev ffmpeg libsm6 libxext6 libxmlsec1-openssl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /usr/app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy project files
COPY . /usr/app/
