from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import rag_tool
from .state_models import ConversationState, Restaurant, MenuItem
from decimal import Decimal

from .initialize import llm


def pre_model_hook(state: ConversationState) -> ConversationState:
    """Pre-model hook to process messages before invoking the model."""

    trimmed_messages = state["messages"][-7:]  # Keep the last 5 messages

    if "user_query" not in state:
        parameters = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert query refiner, skilled at distilling long conversations into concise and effective search queries. Your primary task is to analyze the conversation history between the user and the AI assistant to understand the user's food preferences and intent.

                            1. **Contextual Analysis:** Carefully review the entire conversation, PAYING close attention to the user's last message. If the user makes changes new request, focus on that. Discard the current query if the user has made a new request but with the updated information.

                            2. **Query Formulation:** Formulate a clear and concise search query that captures the essence of the user's request. Role play as the user when generating the query.

                            3. **Length Constraint:** Keep the query brief, ideally within two to three sentences.

                            4. **Relevance:** Ensure the query is relevant to food-related searches, focusing on dishes or cuisines.

                            Ensure the query goes like this: " List all CUISINE_TYPE food options that are DIETARY_RESTRICTIONS and have prices PRICE."CUISINE_TYPE, DIETARY_RESTRICTIONS, and PRICE should be replaced with actual values from the conversation.

                            If DIETARY_RESTRICTIONS and PRICE are not mentioned in the conversation, you can omit them from the query.                      
                            Some of the dietary restrictions can be vegetarian, vegan, gluten-free, nut-free, dairy-free, low-carb, keto, paleo, halal, kosher, pescatarian, low-sodium, high-protein.

                            Extract structured parameters from the query in the following format:
                        - cuisine_type: List of cuisine types mentioned (e.g., ["Italian", "Chinese", "Chicken", "Pizza",etc.])
                        - price: Price range if mentioned this can be optional, DO NOT make up this value if it is not given it can be NULL ("below 25,000 UGX", "No budget","between 30,000 and 50,000 UGX" , or null)
                        - dietary_restrictions: List of dietary restrictions if any, DO NOT make up this value if it is not givenit can be NULL (e.g., ["vegetarian", "gluten-free"]) or null
                        - raw_query: The concise query string you generated.                        
                        Respond with ONLY a Python dictionary containing these parameters and provide the answer to parameters.
                            """
                )
            ]
            + state["messages"]
        )

        return {
            "user_query": parameters.content,
            "llm_input_messages": trimmed_messages,
        }
    else:
        return {
            "llm_input_messages": trimmed_messages,
        }


retrieval: StateGraph = create_react_agent(
    name="retrieval_agent",
    model=llm,
    tools=[rag_tool],
    pre_model_hook=pre_model_hook,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a retrieval agent specializing in food-related information. Your primary task is to retrieve relevant information from databases to answer the user's food query.

            1. **Tool Selection:**
               - Use the rag_tool to retrieve information from the local database. Never halluconate information.
               - Do NOT use any other tools.
               - If you cannot find relevant information, respond with "No relevant information found."

            2. **Information Retrieval:** Retrieve information from the local database sources based on the user's query and the available tools.

            3. **Supervisor Communication:** After completing your task, respond to the supervisor with ONLY the results of your retrieval. Do NOT include any other text or explanations.

            4. **Format:** Ensure your response is in a format that can be easily understood by the supervisor.

            User Food Query: {user_query}

            For extra context, you can view the snippet conversation history below.
            
            Please provide your answer in output field."""
            ),
            MessagesPlaceholder(variable_name="llm_input_messages"),
        ]
    ),
    state_schema=ConversationState,
)
