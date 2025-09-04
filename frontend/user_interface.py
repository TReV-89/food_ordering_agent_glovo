import sys
from pathlib import Path
import streamlit as st
from langchain_core.messages import HumanMessage, BaseMessage
import uuid

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from agents.state_models import SupervisorState
from agents.supervisor_agent import process_messages

# Agent name constant
AGENT_NAME = "Krustie"

st.title("Krustie, The Food Ordering Agent")

# Add clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.state = {
        "messages": [],
        "thread_id": str(uuid.uuid4()),
    }
    st.rerun()

if "state" not in st.session_state:
    st.session_state.state: SupervisorState = {
        "messages": [],
        "thread_id": str(uuid.uuid4()),
    }

# Display messages
for i, message in enumerate(st.session_state.state["messages"]):
    message: BaseMessage
    with st.chat_message(message.type):
        if message.type == "ai":
            if message.name != "supervisor":
                with st.expander(AGENT_NAME):
                    st.write(message.content)
            else:
                # Only display supervisor message if it's the last message
                if i == len(st.session_state.state["messages"]) - 1:
                    st.write(message.content)
        else:
            st.write(message.content)

if prompt := st.chat_input("Please place your order: "):
    new_message = HumanMessage(content=prompt)
    st.session_state.state["messages"].append(new_message)
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner(f"{AGENT_NAME} is thinking..."):
        st.session_state.state = process_messages(st.session_state.state)
    st.rerun()
