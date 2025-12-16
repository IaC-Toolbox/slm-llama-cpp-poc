FROM python:3.12-slim

WORKDIR /app

# Install build tools required by llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir \
    llama-cpp-python \
    huggingface-hub \
    fastapi \
    uvicorn

# Download model at build time
RUN python - <<EOF
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    allow_patterns="*q8_0.gguf",
    local_dir="/models",
    local_dir_use_symlinks=False,
)
EOF

ENV MODEL_PATH=/models/qwen2-0_5b-instruct-q8_0.gguf

COPY . .
CMD ["uvicorn", "slm.main:app", "--host", "0.0.0.0", "--port", "80"]