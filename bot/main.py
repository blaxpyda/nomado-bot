from fastapi import FastAPI
from utils.graph import supervisor
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "kingdieselsbot"

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

user_session = {}


@app.post("/agent")
async def run_agent(request: AgentRequest):
    '''
    Endpoint to run agent with the provided input
    '''

    user_id = 'default'

    if user_id not in user_session:
        user_session[user_id] = {"messages": []}

    user_session[user_id]["messages"].append(HumanMessage(content=request.input))

    #Invoke supervisor with the full history
    result = supervisor.invoke(user_session[user_id])

    #update session with new message
    user_session[user_id] = result

    #Extract last assistant reply
    messages = result.get('messages', [])
    last_bot_message = next(
        (m.content for m in reversed(messages) if m.type != "human"),
        "No response from agent."
    )
    return {'response': last_bot_message}
