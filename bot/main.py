from fastapi import FastAPI
from utils.graph import supervisor
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

app = FastAPI()

# Add cors to allow frontend commmunication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    input: str


@app.post("/agent")
async def run_agent(request: AgentRequest):
    '''
    Endpoint to run agent with the provided input
    '''
    #Prepare the initial state for the graph
    initial_state = {
        "messages": [
            HumanMessage(content=request.input)
        ]
    }

    #Invoke supervisor with the initial state
    result = await supervisor.invoke(initial_state)

    response_content = result['messages'][-1].content if result['messages'] else "No response from agent."
    return {"response": response_content}
