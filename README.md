# SLM Llama.cpp Microservice

A production-ready FastAPI microservice for running Small Language Models (SLMs) locally using llama-cpp-python. This service provides a lightweight alternative to cloud-based LLM inference with lower latency and reduced costs.

## Overview

This microservice wraps the Qwen2-0.5B-Instruct model in a FastAPI server, enabling local inference without requiring GPU acceleration. The service is containerized and ready for deployment on AWS or any Docker-compatible infrastructure.

## Features

- **Local Inference**: Run SLM inference without external API dependencies
- **FastAPI Server**: RESTful API with automatic documentation
- **Docker Ready**: Pre-built container image with model baked in
- **Production Optimized**: Model caching, health checks, and CORS support
- **CPU Compatible**: Runs on standard CPUs using quantized models (GGUF format)

## Prerequisites

- Python 3.12+
- Docker (for containerized deployment)
- 4GB+ available disk space (for model storage)

## Local Development

### Installation

```bash
# Install dependencies using uv
uv sync
uv add llama-cpp-python
uv add huggingface-hub
uv add fastapi
uv add uvicorn
```

### Configuration

Set the model path in your `.env` file:

```bash
export MODEL_PATH=~/.cache/huggingface/hub/models--Qwen--Qwen2-0.5B-Instruct-GGUF/snapshots/<snapshot-id>/qwen2-0_5b-instruct-q8_0.gguf
```

### Running Locally

```bash
uv run uvicorn slm.main:app --host 0.0.0.0 --port 80 --reload
```

## API Endpoints

### Health Check

```bash
GET /health
```

Returns service health status.

### Generate Completion

```bash
POST /generate
Content-Type: application/json

{
  "prompt": "Your prompt here"
}
```

**Example Request:**

```bash
curl --location 'http://127.0.0.1:80/generate' \
--data '{
  "prompt": "hello"
}'
```

**Example Response:**

```json
{
  "id": "cmpl-7771e87d-359e-4f4f-8b00-60db5bfdbc80",
  "object": "text_completion",
  "created": 1765886188,
  "model": "/models/qwen2-0_5b-instruct-q8_0.gguf",
  "choices": [
    {
      "text": "Generated text response",
      "index": 0,
      "logprobs": null,
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 1,
    "completion_tokens": 16,
    "total_tokens": 17
  }
}
```

## Docker Deployment

### Using Docker Compose

```bash
docker compose up
```

### Building the Image

```bash
docker build -f Dockerfile -t slm-llama-cpp-poc .
```

### Running the Container

```bash
docker run -d --name slm-poc -p 80:80 slm-llama-cpp-poc
```

## AWS Deployment

The service can be deployed to AWS EC2 instances. Use the following user data script for initialization:

```bash
#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker $USERNAME

sudo docker run -d --name slm-poc -p 80:80 <your-docker-image>:<tag>
```

**Important**: Build your Docker image on Linux (e.g., using GitHub Actions) to ensure CPU architecture compatibility with EC2 instances.

## CI/CD

The repository includes GitHub Actions workflow for automated Docker image building and publishing to Docker Hub. See `.github/workflows/build-image.yaml` for details.

### Required Secrets

Set these secrets in your GitHub repository:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

## Model Information

- **Model**: Qwen2-0.5B-Instruct-GGUF
- **Quantization**: Q8_0 (8-bit quantization)
- **Size**: ~4GB
- **Format**: GGUF (optimized for CPU inference)
- **Source**: [Hugging Face](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct-GGUF)

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ llama-cpp   │
│   Python    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  GGUF Model │
│  (Local)    │
└─────────────┘
```

## Performance Considerations

- **Cold Start**: Initial model loading takes several seconds
- **Warm Requests**: Subsequent requests are significantly faster due to model caching
- **Context Window**: Default n_ctx=2048 tokens
- **Threads**: Default n_threads=8 (adjust based on CPU cores)

## Repository

[https://github.com/vvasylkovskyi/slm-llama-cpp-poc](https://github.com/vvasylkovskyi/slm-llama-cpp-poc)
