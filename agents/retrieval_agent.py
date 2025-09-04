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

    trimmed_messages = state["messages"][-10:]  # Keep the last 10 messages

    if "user_query" not in state:

        parameters = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert query refiner, skilled at distilling long conversations into concise and effective search queries. Your primary task is to analyze the conversation history between the user and the AI assistant to understand the user's food preferences and intent.

                            1. **Contextual Analysis:** Carefully review the entire conversation, paying close attention to the user's last message to identify their immediate needs.

                            2. **Query Formulation:** Formulate a clear and concise search query that captures the essence of the user's request. Role play as the user when generating the query.

                            3. **Length Constraint:** Keep the query brief, ideally within two to three sentences.

                            4. **Relevance:** Ensure the query is relevant to food-related searches, focusing on dishes or cuisines.

                            Ensure the query goes like this: " List all CUISINE_TYPE food options that are DIETARY_RESTRICTIONS within PRICE range."CUISINE_TYPE, DIETARY_RESTRICTIONS, and PRICE should be replaced with actual values from the conversation.

                            If DIETARY_RESTRICTIONS and PRICE are not mentioned in the conversation, you can omit them from the query.
                            
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


def post_model_hook(state: ConversationState) -> ConversationState:
    """Process the output to structure restaurant and menu data."""
    output = state.get("output", {})

    try:
        restaurants = []

        for restaurant_data in output.get("restaurants", []):
            menu_items = [
                MenuItem(
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    price=Decimal(str(item.get("price", "0"))),
                    promotion=item.get("promotion", False),
                )
                for item in restaurant_data.get("menu_items", [])
            ]

            restaurant = Restaurant(
                name=restaurant_data.get("name", ""), menu_items=menu_items
            )
            restaurants.append(restaurant)

        return {
            "user_query": state.get("user_query", {}),
            "output": {"restaurants": restaurants},
        }

    except Exception as e:
        return {"output": f"Error processing restaurants: {str(e)}"}


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

            3. **Concise Response:** Provide a concise answer that directly addresses the user's query.

            4. **Supervisor Communication:** After completing your task, respond to the supervisor with ONLY the results of your work. Do NOT include any other text or explanations.

            5. **Format:** Ensure your response is in a format that can be easily understood by the supervisor.

            User Food Query: {user_query}

            For extra context, you can view the snippet conversation history below.
            
            Please provide your answer in output field."""
            ),
            MessagesPlaceholder(variable_name="llm_input_messages"),
        ]
    ),
    state_schema=ConversationState,
)
