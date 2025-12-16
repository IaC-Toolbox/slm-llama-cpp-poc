FROM python:3.12-slim

WORKDIR /app

# Install deps
RUN pip install llama-cpp-python huggingface-hub fastapi uvicorn

# Download model at build time
RUN python - <<EOF
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    filename="*q8_0.gguf",
    local_dir="/models",
)
EOF

ENV MODEL_PATH=/models/qwen2-0_5b-instruct-q8_0.gguf

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]