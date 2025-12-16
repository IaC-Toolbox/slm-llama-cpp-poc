import os
from fastapi.concurrency import asynccontextmanager
from llama_cpp import Any, Llama
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    global llm
    llm = Llama(
        model_path=os.environ["MODEL_PATH"],
        n_ctx=2048,
        n_threads=8,
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
