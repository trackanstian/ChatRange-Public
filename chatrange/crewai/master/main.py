import os
from crewai import Agent, Task, Crew, Process
from .agents import TabletopAgents
from .tasks import TabletopTasks
from textwrap import dedent
from chatrange.open_ai import OpenAIClient, OpenAIMessages

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

os.environ["SERPER_API_KEY"] = os.getenv('SERPER_DEV_API_KEY', "")
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY', "")

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

#from langchain.tools import DuckDuckGoSearchRun
#search_tool = DuckDuckGoSearchRun()


# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py


class CyberExerciseCrew:
    def __init__(self, objectives: list = [], outcomes: list = [], uuid: str = "", scenario: str = "", target: str = ""):
        self.objectives = objectives
        self.target = target
        self.outcomes = outcomes
        self.uuid = uuid
        self.scenario = scenario

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TabletopAgents()
        tasks = TabletopTasks(
            objectives = self.objectives,
            target = self.target,
            uuid=self.uuid,
            scenario=self.scenario
        )

        # Define your custom agents and tasks here
        threat_hunter = agents.threat_hunter()
        cybersecurity_researcher = agents.cybersecurity_researcher()



        # Custom tasks include agent name and variables as input
        define_situation = tasks.define_situation(agent=threat_hunter)
        create_setting = tasks.create_setting(context=[define_situation], agent=cybersecurity_researcher)


        # Define your custom crew here
        crew = Crew(
            agents=[threat_hunter, cybersecurity_researcher],
            tasks=[define_situation, create_setting],
            process=Process.sequential,
            #manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),  # Mandatory for hierarchical process
            verbose=True,
        )


    
        result = crew.kickoff()

        returnObject = {
            "result": result,
            "stats": crew.usage_metrics
        }

        return returnObject
    

class CaseStudiesCrew:
    def __init__(self, incident_type: str = "", uuid: str = ""):
        self.incident_type = incident_type
        self.uuid = uuid

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TabletopAgents()
        tasks = TabletopTasks(
            incident_type=self.incident_type,
            uuid=self.uuid
        )

        # Define your custom agents and tasks here
        ciso = agents.ciso()
        data_expert = agents.data_expert()
        cybersecurity_researcher = agents.cybersecurity_researcher()



        # Custom tasks include agent name and variables as input
        get_mitre_techniques = tasks.get_mitre_techniques(agent=data_expert)
        research_case_studies = tasks.research_case_studies(agent=ciso)
        determine_categories = tasks.determine_categories(agent=data_expert)
        #create_json_technique = tasks.create_json_technique(agent=data_expert, context=[research_case_studies])
        find_real_world_examples = tasks.find_real_world_examples(agent=ciso, context=[research_case_studies])
        get_references = tasks.get_references(agent=cybersecurity_researcher, context=[research_case_studies])


        # Define your custom crew here
        crew = Crew(
            agents=[ciso, cybersecurity_researcher],
            tasks=[get_mitre_techniques, determine_categories, research_case_studies, find_real_world_examples, get_references],
            process=Process.sequential,
            #manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),  # Mandatory for hierarchical process
            verbose=True,
        )

        result = crew.kickoff()

        returnObject = {
            "result": result,
            "stats": crew.usage_metrics
        }

        return returnObject
    
class CaseResearchCrew:
    def __init__(self, case: str = "", case_id: int = 0,  uuid: str= ""):
        self.case = case
        self.case_id = case_id
        self.uuid = uuid

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TabletopAgents()
        tasks = TabletopTasks(
            case=self.case,
            case_id=self.case_id,
            uuid=self.uuid
        )

        # Define your custom agents and tasks here
        data_expert = agents.data_expert()
        ciso = agents.ciso()
        cybersecurity_researcher = agents.cybersecurity_researcher()

        # Custom tasks include agent name and variables as input
        research = tasks.research(agent=cybersecurity_researcher)


        # Define your custom crew here
        crew = Crew(
            agents=[ciso, cybersecurity_researcher],
            tasks=[research],
            process=Process.sequential,
            #manager_llm=ChatOpenAI(temperature=0, model="gpt-4-0125-preview"),  # Mandatory for hierarchical process
            verbose=True,
        )

        result = crew.kickoff()

        returnObject = {
            "result": result,
            "stats": crew.usage_metrics
        }

        return returnObject    


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to ChatRange")
    print("-------------------------------")
    #var1 = input(dedent("""Enter variable 1: """))
    #var2 = input(dedent("""Enter variable 2: """))

    custom_crew = CyberExerciseCrew()
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)