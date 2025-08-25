from pydantic import HttpUrl
from typing import List, Optional
from langgraph.prebuilt.chat_agent_executor import AgentState
from decimal import Decimal
from typing_extensions import TypedDict, Annotated


class MenuItem(TypedDict):
    """
    Represents a single item on a restaurant's menu, including details such as name, description, price, category, image, and availability.
    """

    name: Annotated[str, "Name of the menu item"]
    description: Optional[Annotated[str, "Description of the menu item"]]
    price: Annotated[Decimal, "Price of the menu item"]
    category_id: Optional[Annotated[str, "ID of the category this item belongs to"]]
    image_url: Annotated[Optional[HttpUrl], "Image URL for the menu item"]
    promotion: Annotated[bool, "Whether the item is on promotion"] = False
    is_available: Optional[Annotated[bool, "Whether the item is currently available"]] = True


class Category(TypedDict):
    """
    Represents a category of food within a restaurant, including food types, promotion types, and whether it is top rated.
    """

    food_types: Annotated[List[str], "List of food types in this category"]
    promotion_types: Annotated[List[str], "List of promotion types for this category"]
    top_rated: Annotated[bool, "Whether this category is top rated"] = False


class Restaurant(TypedDict):
    """
    Represents a restaurant, including its name, description, rating, categories, menu items, delivery information, and open status.
    """

    name: Annotated[str, "Name of the restaurant"]
    description: Annotated[str, "Description of the restaurant"]
    rating: Annotated[float, "Rating of the restaurant"]
    categories: Annotated[List[Category], "List of categories in the restaurant"]
    menu_items: Annotated[List[MenuItem], "List of menu items in the restaurant"]
    delivery_time: Annotated[float, "Estimated delivery time in minutes"]
    delivery_fee: Annotated[Decimal, "Delivery fee for the restaurant"]
    is_open: Annotated[bool, "Whether the restaurant is currently open"] = True


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
    price: Annotated[str, "Price range requested by the user"]
    dietary_restrictions: Annotated[
        List[str], "Dietary restrictions specified by the user"
    ]


class UserQuery(TypedDict):
    """
    Represents a user's query, including the raw query string and the extracted structured parameters.
    """

    raw_query: Annotated[str, "The raw query string from the user"]
    parameters: Annotated[
        QueryParameters, "Structured query parameters extracted from the user query"
    ]


class ConversationState(AgentState):
    """
    State model for a conversation, containing the user's query and the generated output or response.
    """

    user_query: Annotated[UserQuery, "The user's query and extracted parameters"]
    output: Annotated[str, "The output or response generated"]
