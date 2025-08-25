from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .state_models import ConversationState
from .tools import final_fee

from .initialize import llm


generator: StateGraph = create_react_agent(
    name="generator_agent",
    model=llm,
    tools=[final_fee],
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a response generator agent. Your job is generate a user friendly response for
                the user based on the information given to you from the supervisor agent.     
           Your response must include answer exactly what the user wants. 
           You can use the final_fee tool to calculate the final fee by adding the delivery fee and the price of the menu item.  
        User Food Query: {user_query}

        For extra context, you can view the snippet conversation history below."""
            ),
            MessagesPlaceholder(variable_name="output"),
        ]
    ),
    state_schema=ConversationState,
)
