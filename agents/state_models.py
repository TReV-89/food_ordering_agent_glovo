from typing import List, Optional
from langgraph.prebuilt.chat_agent_executor import AgentState
from typing_extensions import TypedDict, Annotated


class SupervisorState(AgentState):
    """
    State model for the supervisor agent, tracking the unique thread ID for a conversation.
    """

    thread_id: Annotated[str, "Unique identifier for the conversation thread"]


class QueryParameters(TypedDict):
    """
    Represents structured parameters extracted from a user's query, such as cuisine type, price range, and dietary restrictions.
    """

    cuisine_type: Annotated[List[str], "List of cuisine types requested by the user"]
    price: Optional[Annotated[str, "Price range requested by the user"]]
    dietary_restrictions: Optional[
        Annotated[List[str], "Dietary restrictions specified by the user"]
    ]
    raw_query: Annotated[str, "The raw query string from the user"]


class UserQuery(TypedDict):
    """
    Represents a user's query, including the raw query string and the extracted structured parameters.
    """

    parameters: Annotated[
        QueryParameters, "Structured query parameters extracted from the user query"
    ]


class ConversationState(AgentState):
    """
    State model for a conversation, containing the user's query and the generated output or response.
    """

    user_query: Annotated[UserQuery, "The user's query and extracted parameters"]
    llm_input_messages: Annotated[str, "Messages to be sent to the language model"]
    output: Annotated[str, "The generated response or output"]
