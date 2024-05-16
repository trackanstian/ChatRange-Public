import streamlit as st
from streamlit_tags import st_tags
import base64
import json
import logging
import uuid
from chatrange.redis import get_redis_client
import datetime
import os


#Custom imports
from chatrange.helpers import dprint

from chatrange.open_ai import OpenAIClient, OpenAIMessages
from chatrange.redis import get_redis_client

#Start Redis
redis_client = get_redis_client()

sessions = ["session"]
load_sessions = ["session", "main","exercise_objectives", "threat_intel", "generator", "cases"]

# Set the Session variables we need
if 'session' not in st.session_state:
    st.session_state['session'] = str(uuid.uuid4())


# Function to get base64 string of an image
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Function to add custom CSS with base64 background image
def add_custom_css(base64_string):
    css = f"""
    <style>
    .header {{
        background-image: url('data:image/png;base64,{base64_string}');
        background-size: cover;
        background-repeat: no-repeat;
        height: 300px; /* Adjust the height as needed */
    }}
    /* Additional custom CSS can go here */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def ensure_time_object(time_input, time_format="%H:%M:%S"):
    if isinstance(time_input, str):
        # Convert string to datetime.time object
        return datetime.datetime.strptime(time_input, time_format).time()
    elif isinstance(time_input, datetime.time):
        # If it's already a datetime.time object, return it directly
        return time_input
    else:
        # If the input is neither a string nor a datetime.time object, raise an error
        raise TypeError("The input must be either a string or a datetime.time object.")

def create_folder(path: str):
    """
    Create a folder at the specified path if it doesn't already exist.

    Args:
        path (str): The path where the folder should be created.

    Returns:
        None
    """
    path = f"{path}\{st.session_state['session']}"
    if not os.path.exists(path):
        os.makedirs(path)

# Streamlit page layout
st.set_page_config(page_title='ChatRange')

# Convert image to base64 and add custom CSS
image_base64 = get_base64_of_image("cyber_range_chat.png")
add_custom_css(image_base64)

# Create a header section with the background image
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

st.title('ChatRange')
st.markdown('Welcome to ChatRange, a tool for helping you create Cyber training exercise scenarios.')

st.markdown(f"""We generate scenarios by using two methods:
- **Prompt Engineering**:  This is a process where static prompts are used for generating the content based on the user's input.
- **Autonomous AI Agents (AAI)**: This is a process where the Automnoums AI Agents agents will generate the content based on conversation with each other.""")

st.markdown('This project is part of a Master Thesis at the Norwegian University of Science and Technology (NTNU).')


st.header('Session ID')
st.markdown("This ID is used to save your session. If you want to continue working on your previous scenario, replace the ID with your own and click on the button below.")

st.markdown('e62b4422-9b6f-4390-b82e-aacaa8363148')

session_id = st.text_input('Session ID', st.session_state['session'])
if st.button('Load Session'):
    # Load from Redis
    for session in load_sessions:
        st.session_state[session] = json.loads(redis_client.get(f"{str(session_id)}_{session}"))
        create_folder("GenDat/crewai/")
    st.text(f"Loaded session {session_id}")

# Save to Redis
for session in sessions:
    if (st.session_state[session] != None):
        redis_client.set(f"{str(st.session_state['session'])}_{session}", str(json.dumps(st.session_state[session], default=str)))
        redis_client.close()

