from langgraph.graph import START, END, StateGraph, MessagesState
from .agents import make_booking_agent, search_agent, supervisor_agent

#Define the multi-agent supervisor graph
supervisor = (
    StateGraph(MessagesState)
    .add_node(supervisor_agent, destination=("search_agent","make_booking_agent", END))
    .add_node(search_agent)
    .add_node(make_booking_agent)
    .add_edge(START, "supervisor_agent")
    # always return back to the supervisor
    .add_edge("search_agent", "supervisor_agent")
    .add_edge("make_booking_agent", "supervisor_agent")
    .compile()
)
