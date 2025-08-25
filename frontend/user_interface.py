import streamlit as st
from langchain_core.messages import HumanMessage, BaseMessage


from backend.pydantic_state_models import SupervisorState, process_messages
import uuid

st.title("Online Food Ordering Agent")

if "state" not in st.session_state:
    st.session_state.state: SupervisorState = {
        "messages": [],
        "thread_id": str(uuid.uuid4()),
    }

for message in st.session_state.state["messages"]:
    message: BaseMessage
    with st.chat_message(message.type):
        if message.type == "ai":
            if message.name != "supervisor":
                with st.expander(message.name):
                    st.write(message.content)
            else:
                st.write(message.content)
        else:
            st.write(message.content)

if prompt := st.chat_input("Enter your message:"):
    new_message = HumanMessage(content=prompt)
    st.session_state.state["messages"].append(new_message)
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking...."):
        st.session_state.state = process_messages(st.session_state.state)
    st.rerun()
