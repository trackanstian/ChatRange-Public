import json
import os

import requests
from crewai import Agent, Task
from crewai_tools import tool
from langchain_openai import ChatOpenAI

OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

class SuggesterTools:

    @tool('Suggest a better query')
    def run(query: str) -> str:
        """
        Suggests a better query for a given search query.

        Args:
            query (str): The original search query.

        Returns:
            str: The suggested query.

        """
        agent = Agent(
            role='Data sugester',
            goal='Finding amazing solutions when you are stuck with a problem.',
            backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
            llm=OpenAIGPT35,
            allow_delegation=False,
            tools=[]
            )

        task = Task(
            agent=agent,
            description=f'Suggest a better query for the following search: "{query}"'
        )

        summary = task.execute()
        return summary