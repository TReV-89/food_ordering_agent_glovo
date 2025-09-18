from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from state_models import ConversationState
from tools import rag_tool
from initialize import llm


def pre_model_hook(state: ConversationState) -> ConversationState:
    """Pre-model hook to process messages before invoking the model."""

    trimmed_messages = state["messages"][-5:]  

    if "user_query" not in state:
        query = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert in organizing information about meals into a nice readable formatted query for the generator agent.
                    Information provided by the supervisor agent includes  menu items, and prices.
                    Carefully analyze the conversation history between the user and the AI assistant.
                    **Contextual Analysis:** Carefully review the entire conversation, PAYING close attention to the user's last message. If the user makes changes new request, focus on that. Discard the current query if the user has made a new request but with the updated information.
                    Extract the information concerning the meals and their prices.
                    The query generated should guide the generator agent on producing a perfect response. Make sure the query is in the perspective of the user.
                    The query should be along the lines of asking the generator agent to create a user-friendly response based on the information provided by the supervisor agent.
                    The query will be forwarded to the generator agent for further processing.
                    The query should include all necessary details for generating an accurate and helpful response.
                    Ensure the query is clear, concise, and directly addresses the user's query.
                    Below is an example of how the formatted query should be structured:
                    - MEAL_NAME costs PRICE
                    - MEAL_NAME costs PRICE
                    - MEAL_NAME costs PRICE
                    ....etc. where MEAL_NAME is the name of the meal and PRICE is the price of the meal.
                    All prices of the meals should be in UGX.
                    NEVER make up prices. Only use the information provided by the supervisor agent.
                    NEVER include any information that is not provided by the supervisor agent.
                    ENSURE the query is in the perspective of the user e.g " I would like you to generate a user-friendly reponse based on the the information provided:.....".
                    """
                )
            ]
            + trimmed_messages
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
    tools=[rag_tool],
    pre_model_hook=pre_model_hook,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a response generator agent specializing in food-related information. Your primary task is to generate user-friendly responses based on the information provided by the supervisor agent.

1. **Information Synthesis:** Carefully review the information provided by the supervisor agent, including menu items and prices.

2. **Response Generation:** Generate a clear, concise, and user-friendly response that DIRECTLY addresses the user's query.

3. **Recommendation Limit:** When recommending meals , provide at all options, preferably those with prices attached.

4. **Accuracy:** NEVER make up prices. Only use the information provided by the supervisor agent.

5. **User Intent:** Ensure your response accurately reflects the user's intent and preferences, as indicated in the conversation history.

Never use the rag_tool to retrieve information from the database. You should ONLY use the information provided by the supervisor agent.

"""
            ),
            HumanMessage(content="Query:{user_query}"),
            MessagesPlaceholder(variable_name="llm_input_messages"),
        ]
    ),
    state_schema=ConversationState,
)
