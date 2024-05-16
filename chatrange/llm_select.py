from retry import retry
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import json
import logging
import sys
import uuid
import json

#Custom imports
from chatrange.helpers import dprint
from chatrange.redis import get_redis_client

#Clients
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from chatrange.open_ai import OpenAIClient, OpenAIMessages

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY', "")
MODEL_FILE = os.getenv('MODEL_FILE', "models.json")


def load_json_config(file_path):
    """
    Load a JSON configuration file.
    
    :param file_path: Path to the JSON configuration file.
    :return: A dictionary with the configuration.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


def select_model(messages: OpenAIMessages = None, use: str = ""):

    #Load the config file
    config_path = 'GenDat/config/'+MODEL_FILE
    config = load_json_config(config_path)

    dataObject = {}

    for model_config in config:
        if model_config['use'] == use:
            

            #If the model is used for static promting this is the Client
            if model_config['type'] == "openai":
                dataObject['model'] = OpenAIClient(messages=messages, model_type=model_config['model'], temperature=model_config['temperature'], max_tokens=model_config['max_tokens'])
            
            # If the model is used to agents, we need to use the chat client
            elif model_config['type'] == "openai_chat":
                dataObject['model'] = ChatOpenAI(model_name=model_config['model'], temperature=model_config['temperature'], max_tokens=model_config['max_tokens'])
            
            #For GROQ this must be used
            elif model_config['type'] == "groq":
                dataObject['model'] = ChatGroq(model_name=model_config['model'], temperature=model_config['temperature'], groq_api_key=GROQ_API_KEY)

            #This is for local models using Litellm Proxy - https://docs.litellm.ai/docs/proxy/quick_start
            elif model_config['type'] == "litellm":
                dataObject['model'] =  ChatOpenAI(model_name=model_config['model'], base_url=model_config['base_url'], temperature=model_config['temperature'])
            
            else:
                dataObject['model'] = None

            # Add the model config to the data object
            dataObject["config"] = model_config

            return dataObject
    
    return None