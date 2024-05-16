from dotenv import load_dotenv
import os
import logging
import json
from chatrange.logger import Logger

conversation_logger = Logger("conversation")
app_logger = Logger("app")

def nav_to(url, st):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)


def dprint(message, log: str = "default", level=logging.INFO):
    """
    Prints the given message to the specified log with the specified logging level.

    Args:
        message (str): The message to be printed.
        log (str, optional): The name of the log. Defaults to "default".
        level (int, optional): The logging level. Defaults to logging.INFO.
    """
    app_logger.log(message, level)

    if os.getenv('DEBUG') == "true":
        print("["+logging.getLevelName(level)+"] "+str(message))

def conversation(content, role:str , log: str = "conversation", level=logging.INFO):
    """
    Prints the given message to the specified log with the specified logging level.

    Args:
        message (str): The message to be printed.
        log (str, optional): The name of the log. Defaults to "default".
        level (int, optional): The logging level. Defaults to logging.INFO.
    """
    conversation_logger.log(f"[{role}] {content}", level)

    if os.getenv('DEBUG') == "true":
        print("["+logging.getLevelName(level)+"] "+str(content))


def load_file(file_path):
    """
    Load JSON data from a file located at a given relative path.

    :param file_path: Relative path to the JSON file from the script's directory.
    :return: Loaded JSON data.
    """
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(full_path, 'r') as file:
        return json.load(file)
    
    
def format_string(template, variables):
    """
    Formats a template string with placeholders using provided variables.

    :param template: A string with placeholders in curly braces.
    :param variables: A dictionary where keys are the names of placeholders
                        and values are the substitutions for these placeholders.
    :return: The formatted string.
    """
    return template.format(**variables)