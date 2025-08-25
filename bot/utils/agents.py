from .tools import missing_params, get_cheap_flights, make_booking, create_handoff_tool
from langgraph.prebuilt import create_react_agent
import getpass
import os


if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model

# model1 = init_chat_model("llama3-8b-8192", model_provider="groq")
model = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")

query_api_agent = create_react_agent(
    model=model,
    tools=[missing_params, get_cheap_flights],
    prompt=(
        '''
        You are a travel agent helping users find cheap flights.
        Instructions:
         - Assist user in finding the best flight options based on their preferences.
         - You are to use the `missing_params` tool to identify any missing parameters. 
         - Build a JSON object with the flight search parameters for example
           {
           "origin":"MOW","destination":"HKT","depart_date":"2019-11","return_date":"2019-12"
           }
         - If some parameters are still missing, prompt the user to get more context
         - You are to use the `get_cheap_flights` tool and the JSON object to find the best flight options.
        '''
    ),
    name="query_api_agent",
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
assign_to_query_api_agent = create_handoff_tool(
    agent_name="query_api_agent",
    description="Use this tool to handoff to the flight search agent"
)

assign_to_make_booking_agent = create_handoff_tool(
    agent_name="make_booking_agent",
    description="Use this tool to handoff to the flight booking agent"
)

# The supervisor
supervisor_agent = create_react_agent(
  model=model,
  tools=[assign_to_query_api_agent, assign_to_make_booking_agent],
  prompt=(
    '''
    You are a supervisor agent overseeing flight search and booking agents.
    Instructions:
     - Use the appropriate handoff tool to delegate tasks to the flight search or booking agent.
    '''
  ),
  name="supervisor_agent"
)

