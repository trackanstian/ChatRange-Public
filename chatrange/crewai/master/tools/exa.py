from exa_py import Exa
from crewai_tools import tool
import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

EXA_API_KEY = os.getenv('EXA_SEARCH_API_KEY', "")

exa = Exa(api_key=EXA_API_KEY)

class ExaTools:

    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return exa.search(f"{query}", use_autoprompt=True, num_results=5)


    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return exa.find_similar(url, num_results=5)


    @tool
    def get_contents(ids: list[str]):
        """Get the contents of a webpage.
        The ids passed in should be a list of ids returned from `search`.
        """
        return exa.get_contents(ids)