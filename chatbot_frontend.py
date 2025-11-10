# chatbot_frontend.py
import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread-1"}}

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

st.title("Kundan Singh-Powered Chatbot")

# Display conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# Input field (moved outside the loop)
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # Get AI response
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response["messages"][-1].content

    # Add assistant message
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)

