from langchain.tools import tool
from dotenv import load_dotenv
import os
from scrapegraph_py.logger import sgai_logger
from langchain_scrapegraph.tools import SmartScraperTool

load_dotenv()
scrape_graph_key = os.getenv("SGAI_API_KEY")


sgai_logger.set_logging(level="INFO")

smartscraper = SmartScraperTool(api_key=scrape_graph_key)


@tool
def smartscraper_wrapper(keyword: str) -> str:
    """Use this tool to get a url related to the keyword. The keyword must be a type of food like **pizza**, **chicken** or **sharwarma**."""
    food_dict = {
        "chicken": "https://glovoapp.com/ug/en/kampala/kfc-kpa1/",
        "sharwarma": "https://glovoapp.com/ug/en/kampala/meza-shawarma-kpa1/",
        "pizza": "https://glovoapp.com/ug/en/kampala/pizza-stop/",
    }
    url = food_dict.get(keyword.lower())
    return url


@tool
def calculate_final_fee(delivery_fee: float, price: float) -> str:
    """Use this tool to calculate the final fee by adding delivery fee and price of the menu item."""
    return f"UGX {delivery_fee + price}"


final_fee = calculate_final_fee

__all__ = ["smartscraper", "smartscraper_wrapper", "final_fee"]
