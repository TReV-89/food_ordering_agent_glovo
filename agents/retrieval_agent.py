from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import smartscraper, smartscraper_wrapper
from .state_models import ConversationState

from .initialize import llm


def pre_model_hook(state: ConversationState) -> ConversationState:
    """Pre-model hook to process messages before invoking the model."""

    trimmed_messages = state["messages"][-10:]  # Keep the last 10 messages

    if "user_query" not in state:

        query = llm.invoke(
            [
                SystemMessage(
                    content="""You are an expert in converting long conversations into a concise query."
                    Carefully analyze the conversation history between the user and the AI assistant.
                    Extract the most relevant information.
                    Your goal is to understand the user's intent and provide a clear, concise query.
                    The query generated should especially get information about the cuisine type, the dietary restrictions and price fields.
                    The query will be forwarded to the retrieval agent for further processing.
                    Role play as the user asking the question.
                    Your final query should be two to three sentences that captures the essence of the conversation."""
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
                content="""You are a retrieval agent. Your job is to retrieve information from either a database or from the web and use it to answer the user's food query.
           Use musts the tools available to you to retrieve information to help answer the query.
            If the user query has any of the keywords defined below use the smartscraper tool to get the corresponding url.
           The url will be fed into the smartscraper tool with the user food query to get the relevant information from the webpage.
           Your final answer should be concise and directly address the user's query presented.
           After you are done with your tasks, respond to the supervisor directly.
           Respond ONLY with the  resutls of your work, do NOT include ant other text.
           
        User Food Query: {user_query}

        For extra context, you can view the snippet conversation history below."""
            ),
            MessagesPlaceholder(variable_name="output"),
        ]
    ),
    state_schema=ConversationState,
)
