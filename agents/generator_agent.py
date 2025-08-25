from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.state_models import ConversationState

from __init__ import llm


generator_agent: StateGraph = create_react_agent(
    name="retrieval_agent",
    model=llm,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a response generator agent. Your job is generate a user friendly response for\n
                the user based on the information given to you from the supervisor agent.\n     
           Your response must include answer exactly what the user wants.\n         
        User Food Query: {user_query}\n

        For extra context, you can view the snippet conversation history below.\n"""
            ),
            MessagesPlaceholder(variable_name="output"),
        ]
    ),
    state_schema=ConversationState,
)
