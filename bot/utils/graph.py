from langgraph.graph import START, END, StateGraph, MessagesState
from .agents import make_booking_agent, query_api_agent, supervisor_agent

#Define the multi-agent supervisor graph
supervisor = (
    StateGraph(MessagesState)
    .add_node(supervisor_agent, destination=("query_api_agent","make_booking_agent", END))
    .add_node(query_api_agent)
    .add_node(make_booking_agent)
    .add_edge(START, "supervisor_agent")
    # always return back to the supervisor
    .add_edge("query_api_agent", "supervisor_agent")
    .add_edge("make_booking_agent", "supervisor_agent")
    .compile()
)

if __name__ == "__main__":
    initial_input = "I want to book a flight from NYC to LAX."
    response = supervisor.invoke({"input": initial_input})
    print(response)