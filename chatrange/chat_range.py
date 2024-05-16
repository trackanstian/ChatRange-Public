import logging
import sys
from chatrange.open_ai import OpenAIClient, OpenAIMessages
from chatrange.chat_env import BaseConfig
from chatrange.helpers import dprint, conversation, format_string
from chatrange.logger import Logger


class ChatConversation(BaseConfig):
    def __init__(
            self,
            scenario: str,
            phase_name: str = None,
            ):
        super().__init__()
        self.chatconversation = {
            "phase_name": phase_name,
            "phases": [],
            "scenario": scenario
        }
        self.chat_id = []
        self.last_message = None
        pass


    def create_converstions(
            self,
            ) -> None:
        
        #If a specific phase is not specified, we will recruit for all the phases
        if self.chatconversation['phase_name'] is None:
            for phase in self.phases:

                self.phase(phase=phase)

        else:
            phase = next((phase for phase in self.phases if phase.name == self.chatconversation['phase_name']), None)
            if phase is None:
                dprint(message="The phase name does not exist.", level=logging.ERROR)
                raise ValueError("The phase name does not exist.")
            self.phase(phase=phase)



    def phase(self, phase: dict)-> None:
        #Add the phase
        self.chatconversation['phases'].append({"name": phase.name, "tasks": []})

        task_num = 1
        for task in phase.tasks:
            
            #add the task to the phase
            self.chatconversation['phases'][-1]['tasks'].append({"task": task, "task_id": task_num, "roles": []})
    
            task_num += 1

            #Go trough every role
            for role in phase.roles:
                assistant = role.display_name
                #When the roles array is at the end it should use the first role as the user, if not use the next role in the array
                if role.name == phase.roles[-1].name:
                    user = phase.roles[0].name
                    user_display_name = phase.roles[0].display_name
                else:
                    user = phase.roles[phase.roles.index(role)+1].name
                    user_display_name = phase.roles[phase.roles.index(role)+1].display_name

                prompt = format_string(role.prompt, {
                "assistant": assistant,
                "user": user_display_name,
                "role_instruct": role.role_instruct,
                "specification": phase.specification,
                "task": task,
                "scenario": self.chatconversation['scenario'] 
                })


                #Prepare the role
                self.chatconversation['phases'][-1]['tasks'][-1]['roles'].append({"assistant": role.name, "user": user, "prompt": prompt, "summarize": role.summarize})
    

    def chat(self) -> None:
        #Define how many chats is allowed before going on to the next task

        #Then we start by loading the phases, tasks and roles
        for phase in self.chatconversation['phases']:
            for task in phase['tasks']:
                
                #Set a max of 10 chats per task before quitting
                chat_count = 10
                c=0

                while c < chat_count:
                    for role in task['roles']:

                        #Check if the role is in the chat id and has a existing chat, if it has then we continue the conversation
                        chat_id = next((chat for chat in self.chat_id if chat['role'] == role['assistant']), None)
                        chat_index = next((index for index,chat in enumerate(self.chat_id) if chat['role'] == role['assistant']), None)

                        dprint(message=f"Role Assistant: {role['assistant']}", level=logging.DEBUG)

                        chat = OpenAIMessages()

                        if chat_id is not None:
                            #adds the last message
                            chat.add_message(content=self.last_message, role="user")
                            #Create the client
                            client = OpenAIClient(
                                messages=chat,
                                chat_id=chat_id['chat_id']
                            )
                        elif chat_id is None and self.last_message is not None:
                            #Adds the first message
                            chat.add_message(content=role['prompt'], role="system")
                            #adds the last message
                            chat.add_message(content=self.last_message, role="user")
                            client = OpenAIClient(
                                messages=chat,
                            )                           
                        else:
                            #Adds the first message
                            chat.add_message(content=role['prompt'], role="system")
                            client = OpenAIClient(
                                messages=chat,
                            )

                        #Start the chat
                        client.chat()
                        if chat_id is None:
                            self.chat_id.append({"role": role['assistant'], "chat_id": client.chat_id, "messages": 1})
                        else:
                            #Print the role summarization status
                            dprint(message=f"Role {role['assistant']} has {chat_id['messages']} messages and summarization is set to {role['summarize']}", level=logging.DEBUG)
                            
                            #We need to check if the role has a summarize action, this happens when there are more than two answers in the stack.
                            if role['summarize'] == True and chat_id['messages'] > 1:
                                dprint(message="Summarizing answers", level=logging.DEBUG)
                                chat.add_message(content="Instruction: Combine your last two answers into one.", role="user")
                                conversation(content="Instruction: Combine your last two answers into one.", role=role['user'])
                                #Create the client
                                client = OpenAIClient(
                                    messages=chat,
                                    chat_id=chat_id['chat_id']
                                )

                                #Start the chat
                                client.chat()
                                self.last_message = client.last_message
                                conversation(content=client.last_message, role=role['assistant'])

                            self.chat_id[chat_index]['messages'] += 1

                        self.last_message = client.last_message
                        conversation(content=client.last_message, role=role['assistant'])
                        c += 1

                        #If this keyword appear, then we are done with the task and we can go on to the next one
                        if "<TASK_DONE>" in self.last_message:
                            c = chat_count

                #Clear the conversation for the next task
                self.chat_id = []
                self.last_message = None