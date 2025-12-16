import os
from fastapi.concurrency import asynccontextmanager
from llama_cpp import Any, Llama
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    global llm
    llm = Llama.from_pretrained(
        repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF", filename="*q8_0.gguf", verbose=False
    )

    yield


app = FastAPI(lifespan=lifespan)

health_router = APIRouter()


@health_router.get("/health")
async def health() -> Any:
    return {"status": "ok"}


model_router = APIRouter()


@model_router.post("/generate")
async def generate(request: Request) -> Any:
    global llm

    body = await request.json()
    prompt = body.get("prompt", "")

    output = llm(
        prompt,
        stop=["\n"],
        echo=True,
    )
    return output


app.include_router(health_router)
app.include_router(model_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# llm = Llama.from_pretrained(
#     repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF", filename="*q8_0.gguf", verbose=False
# )

# output = llm.create_chat_completion(
#     messages=[
#         {
#             "role": "user",
#             "content": "Hello! How are you?",
#         }
#     ]
# )

# output = llm(
#     "Q: Name the planets in the solar system? A: ",  # Prompt
#     max_tokens=32,  # Generate up to 32 tokens, set to None to generate up to the end of the context window
#     stop=[
#         "Q:",
#         "\n",
#     ],  # Stop generating just before the model would generate a new question
#     echo=True,  # Echo the prompt back in the output
# )  # Generate a completion, can also call create_completion

# print(output)
