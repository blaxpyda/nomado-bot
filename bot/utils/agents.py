from .tools import missing_params, make_search, make_booking, create_handoff_tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv() 

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from langchain.chat_models import init_chat_model

# model1 = init_chat_model("llama3-8b-8192", model_provider="groq")
model = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")

search_agent = create_react_agent(
    model=model,
    tools=[missing_params, make_search],
    prompt=(
        '''
        You are a travel agent helping users find flights.
        Instructions:
         - First, use the `missing_params` tool to identify any missing parameters needed for the flight search.
         - If there are missing parameters, ask the user for the required information.
         - Once all necessary parameters are gathered, use the `make_search` tool to perform the flight search.
        You are to return the data inform of 
         -Airline providing the ticket
         -Price of the ticket
         -Time of departure
        '''
    ),
    name="search_agent",
)

make_booking_agent = create_react_agent(
   model=model,
   tools=[make_booking],
   prompt=(
     '''
     You are a travel agent helping users book flights.
     Instructions:
      - Assist user in booking flights based on their preferences.
      - You are to use the `make_booking` tool to finalize the booking.
      - For purposes of this simulation, you can assume the booking is successful and returns some arbitrary results and a booking link
     '''
   ),
   name="make_booking_agent"
)

#Handoffs
assign_to_search_agent = create_handoff_tool(
    agent_name="search_agent",
    description="Use this tool to handoff to the flight search agent"
)

assign_to_make_booking_agent = create_handoff_tool(
    agent_name="make_booking_agent",
    description="Use this tool to handoff to the flight booking agent"
)

# The supervisor
supervisor_agent = create_react_agent(
  model=model,
  tools=[assign_to_search_agent, assign_to_make_booking_agent],
  prompt=(
    '''
    You are a supervisor agent overseeing flight search and booking agents.
    Instructions:
     - Use the appropriate handoff tool to delegate tasks to the flight search or booking agent.
    '''
  ),
  name="supervisor_agent"
)

