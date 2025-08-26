from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .state_models import ConversationState
from .tools import final_fee

from .initialize import llm


def pre_model_hook(state: ConversationState) -> ConversationState:
    """Pre-model hook to process messages before invoking the model."""

    trimmed_messages = state["messages"][-5:]  # Keep the last 10 messages

    if "user_query" not in state:

        query = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert in converting long conversations into a concise query."
                    Carefully analyze the conversation history between the user and the AI assistant.
                    Extract the most relevant information.
                    Your goal is to understand the user's intent and provide a clear, concise query.
                    The query generated should guide the generator agent on producing a perfect response.
                    The query will be forwarded to the generator agent for further processing.
                    Role play as the user asking the question.
                    Your final query should be two to three sentences that captures the essence of the conversation ensuring
                    it includes all necessary details for generating an accurate and helpful response."""
                )
            ]
            + state["messages"]
        )
        return {
            "user_query": query.content,
            "output": trimmed_messages,
        }
    else:
        return {
            "output": trimmed_messages,
        }


generator: StateGraph = create_react_agent(
    name="generator_agent",
    model=llm,
    tools=[final_fee],
    pre_model_hook=pre_model_hook,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a response generator agent. Your job is generate a user friendly response for
                the user based on the information given to you from the supervisor agent. 
                Please provide at most 3 options for meals or restaurants when the user is looking for food. 
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
