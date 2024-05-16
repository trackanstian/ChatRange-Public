from crewai import Task
from textwrap import dedent
from pydantic import BaseModel
from typing import List
from crewai import Task




# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class TabletopTasks:
    def __init__(
            self, uuid: str,  
            incident_type: str = "",
            organization: str ="ACME Inc", 
            target: str ="IT-Management", 
            purpose: str = " To examine the coordination, collaboration, information sharing, and response capabilities of Acme Inc in reaction to a ransomware incident with third party compromise by phishing.",
            scenario: str =" threat actor targets a third-party vendor through a phishing email as an entry point into Acme Inc networks/systems. Attackers cause computer latency and network access issues and install ransomware on Acme Inc computers.", 
            start: str = "09:00", 
            end: str = "15:00",  
            objectives: list =[]
            ):
        
        self.incident_type = incident_type
        self.uuid = uuid
        self.organization = organization
        self.target = target
        self.purpose = purpose
        self.scenario = scenario
        self.start = start
        self.end = end
        self.objectives = objectives
        self.uuid = uuid

    def create_objective_text(self):
        objective_text = ""
        
        c = 0
        for objective in self.objectives:
            objective_text += dedent(f"""\{objective}
            """)
            c += 1

        return objective_text
    

    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
    
    def define_situation(self, agent):
        return Task(description=dedent(f"""\
            Your job is to analyze the scenario and find the relevant incident types.
                                       
            1. Search for more information about the incident type given.
            2. Create a summary of the incident type.
                                       
            Scenario: {self.scenario}

            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\
            A brief description of the incident types in markdown.
            It must contain the following:
            ## Incident type
            ## Description
            ## MITRE ATT&CK techniques
            """),
            output_file=f"GenDat/crewai/{self.uuid}/threat_intel_01.incident_type.md",
            agent=agent
        )
    
    def create_setting(self, context, agent):
        return Task(description=dedent(f"""\                                      
            Task: Search for a relevant threat actor using the MITRE ATT&CK techniques. You MUST use a real Threat actor for the setting.

            Notes: {self.__tip_section()}     
            """),
            expected_output=dedent(f"""\
            A report of the threat actor markdown.
            It must contain the following:
            ## Threat actor name
            ## Description
            ## Modus operandi
            ## Associated groups
            ## MITRE ATT&CK Techniques Used
            """),
            output_file=f"GenDat/crewai/{self.uuid}/threat_intel_02.setting.md",
            context=context,
            agent=agent
        )


    
    def get_mitre_techniques(self, agent):
        return Task(description=dedent(f"""\

            Task: Get the list of MITRE ATT&CK techniques in the text

            Incident type: "{self.incident_type}"

            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\

            A list of MITRE ATT&CK techniques in json.
            format:
            [
                {{
                    "technique": "string"
                }}
            ]
            """),
            output_file=f"GenDat/crewai/{self.uuid}/case_studies_00.mitre.json",
            agent=agent
        )
    
    def determine_categories(self, agent):
        return Task(description=dedent(f"""\

            Task: Determine what kind of attack the MITRE ATT&CK techniques is used for.
            Examples: Phisihng, ransomware, trojan, insider threat, etc.

            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\

            A list of MITRE ATT&CK techniques and their categories in json.
            format:
            [
                {{
                    "technique": "string",
                    "type_of_attack": "string"
                }}
            ]
            """),
            output_file=f"GenDat/crewai/{self.uuid}/case_studies_01.categories.json",
            agent=agent
        )
    
    def research_case_studies(self, agent):
        return Task(description=dedent(f"""\
            Task: I need the broad categories, such as Phishing or Ransomware, that each MITRE ATT&CK technique falls under, rather than specific examples like spearphishing or CEO fraud. Write a summary for each category.
            
            Description. Only use the technique category when searching for information. Do not include the MITRE ATT&CK ID in your search query. For example, search for "Phishing Emails" instead of "Initial Access: Phishing Emails (T1566)".

            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\
            A summary for each category in json.
            format:
            [
                {{
                    "category": "string",
                    "summary": "string"
                }}
            ]
            """),
            output_file=f"GenDat/crewai/{self.uuid}/case_studies_02.techniques.json",
            agent=agent
        )
       
    def find_real_world_examples(self, agent, context):
        return Task(description=dedent(f"""\
            Task: For each category provided: List of cyber attacks that match the category. At least three examples for each category. 

            Type: This must be a category from the case studies.            

            Example:
            [
                {{"threat": "Hillary Clinton's 2016 presidential campaign spear phishing attacks", "category": "phishing"}},
                {{"threat": "Threat Group-4127 (Fancy Bear) targeting Google accounts", "category": "phishing"}},
                {{"threat": "Whaling attacks targeting senior executives", "category": "phishing"}},
                {{"threat": "WannaCry ransomware attack", "category": "ransomware"}},
                {{"threat": "Taiwan Semiconductor Manufacturing Company (TSMC) ransomware attack", "category": "ransomware"}}
            ]
                                       
            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\
            A list of the examples in JSON. At least three examples for each category.
            format:
            [
                {{"threat":"string", "category":"string"}},
            ]
            """),
            output_file=f"GenDat/crewai/{self.uuid}/case_studies_03.real_world_examples.json",
            agent=agent,
            context=context
        )
    
    def get_references(self, agent, context):
        return Task(description=dedent(f"""\
            Task: I need you to do research for additional resources on the categories presented here. The resrouces must be from reputable sources.
            Find at least four resources for each category.

            Notes: {self.__tip_section()}
            """),
            expected_output=dedent(f"""\
            format:
            [
                {{
                    "category": "string",
                    "title": "string",
                    "url": "link"
                }}
            ]
            """),
            output_file=f"GenDat/crewai/{self.uuid}/case_studies_04.techniques_references.json",
            agent=agent,
            context=context
        )
