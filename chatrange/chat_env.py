import sys
from chatrange.helpers import load_file

#Load the json files
config = {}
config["phases"] = load_file("../GenDat/world/phases.json")
config["roles"] = load_file("../GenDat/world/roles.json")
config["prompts"] = load_file("../GenDat/world/prompts.json")


class BaseConfig():
    def __init__(
            self,
            ):

          #Go trough all the phases in the config and create a Phase object for each
          phases_prepare = []
          for phase in config["phases"]:
               phases_prepare.append(
                    Phase(
                    name=phase['name'],
                    description=phase['description'],
                    roles=phase['roles'],
                    tasks=phase['tasks'],
                    specification=phase['specification']
                    )
               )
          self.phases = phases_prepare
          pass

class Phase():
    def __init__(
            self,
            name: str,
            description: str,
            roles: list,
            tasks: list,
            specification: str
            ) -> None:
          self.name = name
          self.description = description
          self.tasks = tasks
          self.roles_list = roles
          self.specification = specification

          roles_prepare = []
     
          #Go trough all the roles in the phase and create a Role object for each
          for role in roles:
               #If the role is <user> then we will create a default user role, this is used to get input from the user
               if role == "<user>":
                    roles_prepare.append(
                         Role(
                         name="user",
                         display_name="User",
                         description="The user is the person who is being helped by the assistant.",
                         prompt_format="user",
                         role_instruct=[],
                         summarize=False
                         )
                    )
               else:
                    for role_config in config["roles"]:
                         if role_config["name"] == role:
                              roles_prepare.append(
                                   Role(
                                   name=role_config['name'],
                                   display_name=role_config['display_name'],
                                   description=role_config['description'],
                                   prompt_format=role_config['prompt_format'],
                                   role_instruct=role_config['role_instruct'],
                                   summarize=role_config['summarize']
                                   )
                              )
          self.roles = roles_prepare


class Role():
    def __init__(
            self,
            name: str,
            display_name: str,
            description: str,
            prompt_format: str,
            role_instruct: list,
            summarize: str,
            ) -> None:
          self.name = name
          self.display_name = display_name
          self.description = description
          self.role_instruct = role_instruct
          self.summarize = summarize

          for prompt in config["prompts"]:
               if prompt['name'] == prompt_format:
                    self.prompt = prompt['prompt']
               else:
                    raise ValueError("The prompt format "+prompt['name']+" is not defined in the prompts.json file.")
          pass
