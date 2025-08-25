from langchain.tools import tool
from dotenv import load_dotenv
import os
from scrapegraph_py.logger import sgai_logger
from langchain_scrapegraph.tools import SmartScraperTool

from food_ordering_agent_glovo import api_key

load_dotenv()
scrape_graph_key = os.getenv("SGAI_API_KEY")


sgai_logger.set_logging(level="INFO")

smartscraper = SmartScraperTool(api_key = scrape_graph_key)


@tool
