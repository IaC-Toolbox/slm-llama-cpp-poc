import logging
from fastapi import APIRouter, status, Request
from slm.http.response import handle_response

from slm.agent.agent import Agent

logger = logging.getLogger(__name__)


agent_router = APIRouter(prefix="/agent", tags=["Agent"])


@agent_router.post("/run", status_code=status.HTTP_200_OK)
async def run_agent(request: Request):

    agent = Agent()
    
    answer = await agent.run("Hello, can you generate some speech for me?")
    
    return handle_response(
        data={"status": "OK", "response": answer},
        status_code=status.HTTP_200_OK,
    )
