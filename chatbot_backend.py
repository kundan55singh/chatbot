# chatbot_backend.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize model with API key
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

# Define state type
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Define chatbot node
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Create memory saver (checkpointer)
checkpointer = MemorySaver()

# Build graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile graph
chatbot = graph.compile(checkpointer=checkpointer)
