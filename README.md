# slm-llama-cpp-poc

Small Language Model PoC

## Getting Started

Start by syncing dependencies:

```sh
# uv add llama-cpp-python
uv sync
```

## #Install the huggingface-cli

```sh
brew install huggingface-cli
```

### Download Model

```sh
export HF_TOKEN= # Export my Hugging Faces token to improve download speed
hf download Qwen/Qwen2-0.5B-Instruct-GGUF
```
