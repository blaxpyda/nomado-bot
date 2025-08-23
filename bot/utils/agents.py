from tools import missing_params, get_cheap_flights
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
         - Build a JSON object with the flight search parameters that is
           - origin: IATA code of the departure airport
           - destination: IATA code of the arrival airport
           - depart_date: Date of departure
           - return_date: This can be optional for one way flights.
         - You are to use the `get_cheap_flights` tool to find the best flight options.
        '''
    ),
    name = "query_api_agent",
)

if __name__ == "__main__":
    query = "Find me a flight from NYC to LAX departing on 2024-12-20 and returning on 2024-12-30."
    response = query_api_agent.invoke({"input": query})
    print(response)

