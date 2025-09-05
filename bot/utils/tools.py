from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Annotated
from selenium import webdriver

@tool
def missing_params(**kwargs):
    """
    Identify missing parameters for the flight search API.
    """
    required_params = ["origin", "destination", "depart_date", "return_date", "class"]
    missing = [param for param in required_params if param not in kwargs]
    return missing

@tool
def make_search(driver):
    '''
    Perform a flight search using Selenium.
    '''
    driver = webdriver.Chrome()
    driver.get("https://tp.media/r?marker=664449&trs=448817&p=4114&u=https%3A%2F%2Faviasales.com&campaign_id=100")
    # Perform search actions using Selenium
    driver.quit()


@tool
def make_booking(driver):
    '''
    Make a flight booking using Selenium.
    '''
    driver = webdriver.Chrome()
    driver.get("https://tp.media/r?marker=664449&trs=448817&p=4114&u=https%3A%2F%2Faviasales.com&campaign_id=100")
    # Perform booking actions using Selenium
    driver.quit()

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

