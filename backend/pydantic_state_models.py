from pydantic import Field, BaseModel, HttpUrl
from typing import List, Optional
from langgraph.prebuilt.chat_agent_executor import AgentState
from decimal import Decimal


class MenuItem(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the menu item")
    description: str = Field(..., description="What makes up the menu item")
    price: Decimal = Field(..., gt=0, description="Price of the menu item")
    category_id: str = Field(..., description="Category this item belongs to")
    image_url: Optional[HttpUrl] = None
    promotion: bool = False
    is_available: bool = True


class Category(BaseModel):
    food_types: List = Field(..., description="Food types the restaurant has")
    promotion_types: List = Field(..., description="Type of promotion available")
    top_rated: bool = False


class Restaurant(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    rating: float = Field(..., ge=0, le=5)
    categories: List[Category] = Field(default_factory=list)
    menu_items: List[MenuItem] = Field(default_factory=list)
    delivery_time: float = Field(..., gt=0, description="Delivery time in minutes")
    delivery_fee: Decimal = Field(..., description="Delivery fee depending on location")
    is_open: bool = True


class SupervisorState(AgentState):
    thread_id: str


class QueryParameters(BaseModel):
    cuisine_type: Optional[List] = None
    price: Optional[str] = Field(None, pattern=" ....UGX")
    dietary_restrictions: List[str] = Field(default_factory=list)


class UserQuery(BaseModel):
    raw_query: str = Field(..., min_length=1)
    parameters: QueryParameters = Field(default_factory=QueryParameters)


class ConversationState(AgentState):
    query: UserQuery
    output: str
