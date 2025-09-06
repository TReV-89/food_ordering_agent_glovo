import sys
from pathlib import Path
import streamlit as st
from langchain_core.messages import HumanMessage, BaseMessage
import uuid

# --- Custom CSS: Sidebar Tomato Red + Clear Chat Button White + Send Icon Red ---
st.markdown(
    """
    <style>
    /* Sidebar background in Tomato Red */
    section[data-testid="stSidebar"] {
        background-color: #E63946 !important;
    }

    /* Clear Chat button style */
    section[data-testid="stSidebar"] button {
        background-color: white !important;
        color: black !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        font-weight: bold;
        cursor: pointer;
    }

    /* Optional: Hover effect for Clear Chat button */
    section[data-testid="stSidebar"] button:hover {
        background-color: #f2f2f2 !important;
    }

    /* Chat input send button (arrow) */
    div[data-testid="stChatInput"] button {
        background-color: #E63946 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        cursor: pointer;
    }

    /* Optional: Hover effect for send button */
    div[data-testid="stChatInput"] button:hover {
        background-color: #d6343f !important;  /* slightly darker tomato red */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from agents.state_models import SupervisorState
from agents.supervisor_agent import process_messages

# Agent name constant
AGENT_NAME = "Krustie"

# Logo next to title with vertical alignment
logo_path = "images/logo.png"

col1, col2 = st.columns([1, 6], gap="small")
with col1:
    st.image(logo_path, width=200) 
with col2:
    st.markdown(
        "<h1 style='display: flex; align-items: center; margin: 0;'>Krustie, The Food Ordering Agent</h1>",
        unsafe_allow_html=True,
    )


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
    if message.type == "human":
        # Display user messages
        with st.chat_message("user"):
            st.write(message.content)
    elif message.type == "ai" and message.name == "supervisor":
        # Only display supervisor messages
        content = message.content.strip()
        if content:  # Only display if content is not empty
            with st.chat_message("ai"):
                st.write(content)

if prompt := st.chat_input("Please place your order: "):
    new_message = HumanMessage(content=prompt)
    st.session_state.state["messages"].append(new_message)
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner(f"{AGENT_NAME} is thinking..."):
        st.session_state.state = process_messages(st.session_state.state)
    st.rerun()
