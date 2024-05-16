from retry import retry
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import json
import logging
import sys
import uuid

#Custom imports
from chatrange.helpers import dprint
from chatrange.redis import get_redis_client

#Start Redis
redis_client = get_redis_client()

load_dotenv()  # This method will load variables from .env
openai_client = OpenAI(
api_key = os.getenv('OPENAI_API_KEY')
)


# Create the Embedding class
class OpenAIEmbeddings():
    
    def __init__(self):
        self.embeddings = []
        self.response = ""


    @retry(tries=1, delay=2, backoff=2, max_delay=60)
    def get_embedding(self, content: str):
        client = OpenAI()
        self.response = client.embeddings.create(input=content, model="text-embedding-ada-002").data[0].embedding
        pass



#Create the messages Class
class OpenAIMessages():

    def __init__(self):
        self.messages = []

    def add_message(self, content: str, role:str):
        message = {
            "content": content,
            "role": role
        }
        self.messages.append(message)
        pass

    def count_cost_in(self, model):
        if model == "gpt-3.5-turbo-0125":
            return 0.0005
        
        if model == "gpt-3.5-turbo-1106":
            return 0.001
        
        if model == "gpt-4-0125-preview":
            return 0.01
        
        if model == "gpt-4-turbo-preview":
            return 0.01
        
        if model == "gpt-4-1106-preview":
            return 0.01
        
        if model == "gpt-3.5-turbo-0613":
            return 0.0015
        
    
        dprint(message="Model not found", level=logging.ERROR)
        return(0)
        
    def count_cost_out(self, model):
        if model == "gpt-3.5-turbo-0125":
            return 0.0015
                
        if model == "gpt-3.5-turbo-1106":
            return 0.0020
        
        if model == "gpt-4-0125-preview":
            return 0.03
        
        if model == "gpt-4-turbo-preview":
            return 0.03
        
        if model == "gpt-4-1106-preview":
            return 0.03
        
        if model == "gpt-3.5-turbo-0613":
            return 0.0020
        
        dprint(message="Model not found", level=logging.ERROR)
        return(0)
        

class OpenAIClient():
    r"""
    DOCS HERE
    """


    def __init__(
            self, 
            model_type: str = "gpt-3.5-turbo-16k",
            max_tokens: int = 1000,
            temperature: float = 0.2,
            top_p: float = 1.0,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
            messages: OpenAIMessages = [],
            chat_id: str = None,
            schema: dict = None,
            json: bool = False
        ) -> None:

        if not messages:
            dprint(message="The messages argument cannot be empty.", level=logging.ERROR)
            raise ValueError("The messages argument cannot be empty.")

        self.model_type = model_type
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.chat_id = chat_id
        self.system = None
        self.messages = messages
        self.schema = schema
        self.json = json

    @retry(tries=1, delay=2, backoff=2, max_delay=60)
    def chat(self, return_id: bool = True) -> dict:
        dprint(message="==== Running OpenAI query ====",)

        #Generate a chat conversation id
        conversation_id = uuid.uuid4()

        #If this is not none then we have a chat id and we can continue the conversation by loading the chat from redis
        if self.chat_id is not None:
            conversation_id = self.chat_id

            dprint(message="Chat ID is not none, continuing conversation id "+str(conversation_id))
            chat = redis_client.get(str(conversation_id))
            chat = json.loads(chat)

            dprint(message="Chat length  is on load "+str(len(chat)), level=logging.DEBUG)

        else:
            chat = []

        params = {
        "model": self.model_type,
        "frequency_penalty": self.frequency_penalty,
        "max_tokens": self.max_tokens,
        "presence_penalty": self.presence_penalty,
        "top_p": self.top_p,
        "temperature": self.temperature
        }

        if self.schema is not None:
            params["tools"] = [{"type":"function", "function": {"name": "get_schema", "description": "runs a schema control", "parameters": self.schema}}]
            params["tool_choice"] = {"type": "function", "function": {"name": "get_schema"}}

        if self.json:
            params["response_format"] = {"type": "json_object" }

        #Add the new messages to the chat, then remoce them from the messages list 
        for message in self.messages.messages:
            chat.append({"role": message['role'], "content": message['content']})

        params["messages"] = chat

        #Run the query
        chat_completion = openai_client.chat.completions.create(**params)

        #add the latest message to the chat when returned from openai
        chat.append({"role": chat_completion.choices[0].message.role, "content": chat_completion.choices[0].message.content})
        

        #Save the response to redis
        redis_client.set(str(conversation_id), str(json.dumps(chat)))
        
        dprint(message="Completed LLM request")
        if return_id:
            self.chat_id = conversation_id
        self.last_message = chat_completion.choices[0].message.content



