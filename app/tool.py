from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import requests

class State(MessagesState):
    my_var: str


# Define the tools

def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


def get_categories() -> str:
    """ Get the categories of the products."""

    response = requests.get("https://api.escuelajs.co/api/v1/categories")
    categories = response.json()
    category_names = [category["name"] for category in categories]
    return ", ".join(category_names)


tools = [multiply, add, get_categories]

# Define the nodes  

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm = llm.bind_tools(tools, parallel_tool_calls=False)


def assistant(state: State) -> State:
    system_message = SystemMessage(content="Eres un experto en matemáticas y además tienes acceso a las categorías de los productos.")
    
    return {"messages": [llm.invoke([system_message] + state["messages"])]}


# Define the graph

builder = StateGraph(State)

builder.add_node('assistant', assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, 'assistant')
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

graph = builder.compile()