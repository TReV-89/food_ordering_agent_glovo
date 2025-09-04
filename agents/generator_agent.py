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
            "llm_input_messages": trimmed_messages,
        }
    else:
        return {
            "llm_input_messages": trimmed_messages,
        }


generator: StateGraph = create_react_agent(
    name="generator_agent",
    model=llm,
    tools=[final_fee],
    pre_model_hook=pre_model_hook,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a response generator agent specializing in food-related information. Your primary task is to generate user-friendly responses based on the information provided by the supervisor agent.

1. **Information Synthesis:** Carefully review the information provided by the supervisor agent, including restaurant details, menu items, and prices.

2. **Response Generation:** Generate a clear, concise, and user-friendly response that directly addresses the user's query.

3. **Recommendation Limit:** When recommending meals or restaurants, provide at most 3 options, preferably those with prices attached.

4. **Accuracy:** NEVER make up prices or delivery fees. Only use the information provided by the supervisor agent.

5. **Tool Usage:** ONLY use the `final_fee` tool to calculate the final fee by adding the delivery fee and the price of the menu item when the user explicitly asks for it.

6. **User Intent:** Ensure your response accurately reflects the user's intent and preferences, as indicated in the conversation history.

User Food Query: {user_query}

For extra context, you can view the snippet conversation history below."""
            ),
            MessagesPlaceholder(variable_name="llm_input_messages"),
        ]
    ),
    state_schema=ConversationState,
)
