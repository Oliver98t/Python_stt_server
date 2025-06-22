# Use the official Python 3.11.13 slim image as base
FROM python:3.11.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies (including those for building whisper.cpp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    pkg-config \
    wget \
    ca-certificates \
    libopenblas-dev \
    libfftw3-dev \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libswresample-dev \
    libsdl2-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Print Ubuntu version for debugging
RUN cat /etc/os-release

# Set working directory
WORKDIR /workspace

# Copy source code into the container
COPY . .

RUN sh ./whisper.cpp/models/download-ggml-model.sh base.en

# Build whisper.cpp (example: build release binaries)
RUN cd whisper.cpp && cmake -B build && cd build && make -j12

# Default command: show built binaries
CMD ["ls", "-l", "/workspace/build/bin"]
