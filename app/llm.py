from langchain_openai import ChatOpenAI
from typing import TypedDict
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define the state of the agent

class State(MessagesState):
    my_var: str
    customer_name: str


# Define the nodes

system_message = SystemMessage(content="You are a helpful assistant and you expert in Angular, only your answer should be in Angular avoid using other languages")

def node_llm(state: State) -> State:
    print(state)
    return {"messages": [llm.invoke([system_message] + state["messages"])]}


builder = StateGraph(State)

builder.add_node('node_llm', node_llm)

builder.add_edge(START, 'node_llm')
builder.add_edge('node_llm', END)

graph = builder.compile()