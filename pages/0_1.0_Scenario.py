import streamlit as st
from streamlit_tags import st_tags
import base64
import json
import logging
import uuid
from chatrange.redis import get_redis_client
from chatrange.helpers import dprint, conversation, format_string, nav_to
import datetime




#Custom imports
from chatrange.helpers import dprint

from chatrange.open_ai import OpenAIClient, OpenAIMessages
from chatrange.redis import get_redis_client

#If the UUID is not set then go to the Start
if 'session' not in st.session_state:
    nav_to("/", st)

#Start Redis
redis_client = get_redis_client()

sessions = ["main","exercise_objectives", "threat_intel", "generator", "cases"]

#Set the Session variables we need
if 'main' not in st.session_state:
    st.session_state['main'] = {
        "type": "",
        "start_time": "09:00:00",
        "end_time": "16:00:00",
        "type": "Tabletop",
        "participants": "IT-Management",
        "organization": "ACME Inc",
        "purpose": f"To examine the coordination, collaboration, information sharing, and response capabilities of ACME Inc in reaction to a ransomware incident with third party compromise by phishing.",
        "scenario": f"A threat actor targets a third-party vendor through a phishing email as an entry point into ACME Inc networks/systems. Attackers cause computer latency and network access issues and install ransomware on ACME Inc computers.",
        "tokens_out": 0,
        "tokens_in": 0,
        "cost_out": 0,
        "cost_in": 0


    }

if 'exercise_objectives' not in st.session_state:
    st.session_state['exercise_objectives'] = {
    "tuning": "",
    "suggestions": [],
    "generated": [],
    "objectives": [
        "Discuss elements of Acme Inc’s cybersecurity posture.",
	    "Examine Acme Inc’s cybersecurity information sharing procedures and mechanisms.",
	    "Examine Acme Inc’s cyber incident response plans or playbooks."
    ]
}
    
if 'threat_intel' not in st.session_state:
    st.session_state['threat_intel'] = {
    "research": "",
}
    
if 'generator' not in st.session_state:
    st.session_state['generator'] = {
    "parts": "",
    "timeline": "",
    "questions": "",
    }

if 'cases' not in st.session_state:
    st.session_state['cases'] = {
    "research": "",
    "details": []
}

if 'temp_out' not in st.session_state:
    st.session_state['temp_out'] = ""
    




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



# Streamlit page layout
st.set_page_config(page_title='ChatRange')

# Convert image to base64 and add custom CSS
image_base64 = get_base64_of_image("cyber_range_chat.png")
add_custom_css(image_base64)

# Create a header section with the background image
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

st.title('ChatRange')
st.markdown('Welcome to ChatRange, a tool for helping you create Cyber training exercise scenarios. Define your settings for the exercise and then click on the button below to start.')
if st.session_state['main']['type'] == "Tabletop":
    index = 0
elif st.session_state['main']['type'] == "Live":
    index = 0
elif st.session_state['main']['type'] == "Hybrid":
    index = 0
else:
    index = 0


st.session_state['main']['type'] = st.selectbox("Select exercise type", ["Tabletop", "Live (Not ready yet)", "Hybrid (Not ready yet)"], index=index)
st.session_state['main']['start_time'] = st.time_input('Start at', ensure_time_object(st.session_state['main']['start_time']))
st.session_state['main']['end_time'] = st.time_input('End at', ensure_time_object(st.session_state['main']['end_time']))
st.session_state['main']['participants'] = st.text_input('Participants', st.session_state['main']['participants'])
st.session_state['main']['organization'] = st.text_input('Organization', st.session_state['main']['organization'])
st.session_state['main']['purpose'] = st.text_area('What is the purpose?', st.session_state['main']['purpose'])
st.session_state['main']['scenario'] = st.text_area('What is the scenario?', st.session_state['main']['scenario'])
#st.markdown('<a href="/Scenario_Settings" target="_self">Skoden</a>',unsafe_allow_html=True)

# Save to Redis
for session in sessions:
    redis_client.set(f"{str(st.session_state['session'])}_{session}", str(json.dumps(st.session_state[session], default=str)))
    redis_client.close()