from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Annotated
import requests
import os

@tool
def missing_params(**kwargs):
    """
    Identify missing parameters for the flight search API.
    """
    required_params = ["origin", "destination", "depart_date", "return_date"]
    missing = [param for param in required_params if param not in kwargs]
    return missing

@tool
def get_cheap_flights(origin, destination, depart_date, return_date):
    """
    Get cheap flight options from the TravelPayouts API.
    """
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    headers = {
        "Content-Type": "application/json",
        "X-Access-Token": os.getenv("TRAVEL_PAYOUTS_API_KEY")
    }
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if not data.get("success"):
            print("API request failed:", data.get("error", "Unknown error"))
            return None

        flights = data.get("data", {}).get(destination, {})
        if not flights:
            print(f"No flights found from {origin} to {destination} on {depart_date}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
@tool
def make_booking(origin, destination, depart_date, return_date):
    '''
    Make a flight booking. Returns a simple booking link
    '''
    pass

def create_handoff_tool(*, agent_name: str, description: str | None=None):
    name = f"handoff_to_{agent_name}"
    description = description or f"Use this tool to handoff to the {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Handing off to {agent_name} agent.",
            "name": name,
            "tool_call_id": tool_call_id
        }
        return Command(
            goto=agent_name,
            update={**state, "messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,
        )
    return handoff_tool

