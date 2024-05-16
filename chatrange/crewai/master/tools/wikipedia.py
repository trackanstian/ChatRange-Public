from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.retrievers import WikipediaRetriever
from crewai_tools import tool

class WikiPediaTools:

    @tool("Search wikipedia for information")
    def search(query: str) -> str:
        """
        Searches Wikipedia for the given query and returns the result.

        Args:
            query (str): The search query.

        Returns:
            str: The search result.

        """
        search_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        return search_tool.run(query)
    
    @tool("Get wikipedia relevant information")
    def get_info(query: str) -> str:
        """
        Retrieves relevant documents from Wikipedia based on the given query.

        Args:
            query (str): The search query to retrieve information from Wikipedia.

        Returns:
            str: The relevant documents retrieved from Wikipedia.

        """
        retriever = WikipediaRetriever()
        search_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        return retriever.get_relevant_documents(query=query)