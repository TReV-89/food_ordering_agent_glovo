from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import smartscraper, smartscraper_wrapper
from .state_models import ConversationState
from .initialize import llm

import os
scrape_graph_key = os.getenv("SGAI_API_KEY")

def pre_model_hook(state: ConversationState) -> ConversationState:
    """Pre-model hook to process messages before invoking the model."""

    trimmed_messages = state["messages"][-10:]  # Keep the last 10 messages

    if "user_query" not in state:

        query = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert query refiner, skilled at distilling long conversations into concise and effective search queries. Your primary task is to analyze the conversation history between the user and the AI assistant to understand the user's food preferences and intent.

1. **Contextual Analysis:** Carefully review the entire conversation, paying close attention to the user's last message to identify their immediate needs.

2. **Information Extraction:** Extract key details such as:
    - Cuisine type (e.g., Italian, Chinese, Indian)
    - Dietary restrictions (e.g., vegetarian, gluten-free, vegan)
    - Price preferences (e.g., budget-friendly, mid-range, luxury)
    - Specific dishes or ingredients mentioned

3. **Query Formulation:** Formulate a clear and concise search query that captures the essence of the user's request. Role play as the user when generating the query.

4. **Length Constraint:** Keep the query brief, ideally within two to three sentences.

5. **Relevance:** Ensure the query is relevant to food-related searches, focusing on dishes or cuisines.

By following these guidelines, you will generate effective queries that enable the retrieval agent to find the most relevant information for the user.."""
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


retrieval: StateGraph = create_react_agent(
    name="retrieval_agent",
    model=llm,
    tools=[smartscraper, smartscraper_wrapper],
    pre_model_hook=pre_model_hook,
    prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a retrieval agent specializing in food-related information. Your primary task is to retrieve relevant information from databases or the web to answer the user's food query.

            1. **Tool Selection:**
               - If the user query contains keywords like "chicken", "sharwarma", or "pizza", use the `smartscraper_wrapper` tool to get the corresponding URL.
               - Then, use the `smartscraper` tool with the URL and the user's query to extract relevant information from the webpage.
               - If the query doesn't contain those keywords, use your general knowledge and available tools to find the information.

            2. **Information Retrieval:** Retrieve information from the appropriate sources based on the user's query and the available tools.

            3. **Concise Response:** Provide a concise answer that directly addresses the user's query.

            4. **Supervisor Communication:** After completing your task, respond to the supervisor with ONLY the results of your work. Do NOT include any other text or explanations.

            5. **Format:** Ensure your response is in a format that can be easily understood by the supervisor.

            User Food Query: {user_query}

            For extra context, you can view the snippet conversation history below."""
            ),
            MessagesPlaceholder(variable_name="output"),
        ]
    ),
    state_schema=ConversationState,
)
