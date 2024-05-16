from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.wikipedia import WikiPediaTools 
from .tools.exa import ExaTools
from .tools.suggester import SuggesterTools
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from chatrange.llm_select import select_model

exa= ExaTools()
suggester = SuggesterTools()
wikipedia_search = WikiPediaTools()
search_tool = SerperDevTool()
scraper_tool = ScrapeWebsiteTool()

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class TabletopAgents:
    def __init__(self):
        self.model = None

    def data_expert(self):
        model_settings = select_model(use="agent_data_expert")
        return Agent(
            role=dedent("Data Expert"),
            goal=dedent("Want to see data presented in the best possible way according to the expexcations"),
            backstory=dedent("A seasoned expert in formatting data in the best possible way. Known for presenting data in the best possible way according to the expectations."),
            allow_delegation=False,
            verbose=True,
            llm=model_settings['model'],
            memory=True,
            tools=[],
            max_iterations=10
        )

    def ciso(self):
        model_settings = select_model(use="agent_ciso")
    
        return Agent(
            role=dedent("Chief Information Security Officer (CISO)"),
            goal=dedent("Develop and enforce information security policies, manage risk, and ensure compliance with regulations."),
            backstory=dedent("This CISO is a seasoned cybersecurity professional known for safeguarding organizations from cyber threats."),
            allow_delegation=False,
            verbose=True,
            llm=model_settings['model'],
            memory=True,
            tools=[wikipedia_search.search, wikipedia_search.get_info, suggester.run],
            max_iterations=10
        )
   
    def threat_hunter(self):
        model_settings = select_model(use="agent_threat_hunter")

        return Agent(
            role='Specialized Threat Hunter',
            goal=dedent("""Identify and neutralize advanced persistent threats (APTs) within 
                    complex digital environments, employing cutting-edge technology 
                    and methodologies to detect, analyze, and disarm sophisticated 
                    cyber threats before they can exploit vulnerabilities."""),
            backstory=dedent("""An expert in cybersecurity with a keen eye for uncovering 
                         hidden threats, the Threat Hunter has a decorated history 
                         of neutralizing high-profile cyberattacks. With a background 
                         in digital forensics and a passion for cybersecurity innovation, 
                         they have become a pivotal asset in preemptive threat detection 
                         and resolution, safeguarding critical infrastructure from 
                         potential cyber disasters."""),
            allow_delegation=True,
            verbose=True,
            llm=model_settings['model'],
            memory=False,
            tools=[search_tool],
            max_iterations=10
        )

    def cybersecurity_researcher(self):
        model_settings = select_model(use="agent_cybersecurity_researcher")
                                      
        return Agent(
            role='Cybersecurity Researcher',
            goal="""Explore emerging cybersecurity threats, create new defenses, and advance knowledge on cyber protection. Use advanced analytics and innovative research to understand cyber attacks and develop solutions for stronger digital security.""",
            backstory="""Driven by a keen interest in the digital domain and sharp analytical skills, the Cybersecurity Researcher excels in uncovering and combating cyber threats. A specialist with a strong computer science background, their work in threat detection and prevention has established them as a cybersecurity authority. They are dedicated to defending digital infrastructures and ensuring data security against advanced cyber attacks.""",
            allow_delegation=True,
            verbose=True,
            llm=model_settings['model'],
            memory=False,
            tools=[],
            max_iterations=10
        )
