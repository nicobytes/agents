from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the state of the agent

class State(TypedDict):
    my_var: str
    customer_name: str


# Define nodes (agent == node)

def node_1(state: State) -> State:
    state["my_var"] = "Hello"
    state["customer_name"] = "John"
    return state


def node_2(state: State) -> State:
    customer_name = state["customer_name"]
    state["my_var"] = f"Hello {customer_name}"
    return state


def node_3(state: State) -> State:
    return state



# Define the graph

builder = StateGraph(State)

builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)

builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_2', 'node_3')
builder.add_edge('node_3', END)

graph = builder.compile()
