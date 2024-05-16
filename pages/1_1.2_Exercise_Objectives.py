import streamlit as st
import time
import logging
from chatrange.helpers import dprint, conversation, format_string, nav_to
from chatrange.logger import Logger
import json
from chatrange.redis import get_redis_client
import uuid
import pandas as pd
import tiktoken
from textwrap import dedent

import requests
import html2text

from chatrange.open_ai import OpenAIClient, OpenAIMessages
from chatrange.llm_select import select_model

#If the UUID is not set then go to the Start
if 'main' not in st.session_state:
    nav_to("/1.0_Scenario", st)

#Start Redis
redis_client = get_redis_client()

def is_valid_json(json_string):
    try:
        json_object = json.loads(json_string)
        return True
    except json.JSONDecodeError:
        dprint(message="The string is not a valid JSON.", level=logging.ERROR)
        dprint(message=json_string, level=logging.DEBUG)
        dprint(message=str(json.JSONDecodeError), level=logging.DEBUG)
        return False

def get_ai_suggestion(focus: str = None, exercise_type: str = None, participants: str = "", organization: str = "ACME Inc", scenario: str = None):
    chat = OpenAIMessages()


    if focus:
        focus = dedent(f"""
            Focus areas: {focus}
            """)

    message = dedent(f"""
        You are a Chief Information Security Officer (CISO), and you serve as the guardian of your organization's digital assets, implementing robust cybersecurity strategies, leading incident response efforts, and fostering a culture of security awareness and compliance throughout the company. You possess a deep understanding of evolving cyber threats, expert knowledge in risk management, and the ability to communicate effectively with stakeholders at all levels to mitigate risks and ensure the integrity, confidentiality, and availability of critical data and systems.

        Task: Create at least five exercise objectives for a exercise. The exercise objecives MUST be relative to the exercise type and participants. 
        You MUST include the organization name in each objective text.

        Exercise type: {exercise_type}
        Participants: {participants}
        Organization: {organization}
        Scenario: {scenario}

        ==RULES==
        Answers must be in a valid JSON array.
        You must focus your answers on this: {focus}

        Examples: 
        Determine the effectiveness of the cyber education provided to the training audience prior to the start of the exercise
        Assess effectiveness of the organization’s/exercise’s incident reporting and analysis guides for remedying deficiencies


        Output format:
        ["This is an suggestion", "This is another suggestion", "This could be the third suggestion"]
        """)
    chat.add_message(content=message, role="system")

    #Load the model data
    model_data = select_model(messages=chat, use="exercise_objectives")
    client = model_data["model"]

    # Chat uintil we return a valid JSON
    errors = 0
    while True and errors < 5:
        return_id = False
        client.chat(return_id=return_id)

        # Check if client.last_message is valid JSON
        if is_valid_json(client.last_message):
            return_id = client.chat_id
            chat.add_message(content="...", role="user")
            break

        errors += 1

    returnInfo  = {
        "last_message": client.last_message
    }

    # Tiktoken
    #Fix for GPT-4o for tiktoken
    if model_data["config"]["model"] == "gpt-4o":
        encoding = tiktoken.get_encoding("o200k_base")
    else:
        encoding = tiktoken.encoding_for_model(model_data["config"]["model"])
    st.session_state['main']['tokens_out'] += len(encoding.encode(message))
    st.session_state['main']['cost_out'] += ((len(encoding.encode(message))/1000) * model_data["config"]["price_in"])

    st.session_state['main']['tokens_in'] += len(encoding.encode(client.last_message))
    st.session_state['main']['cost_in'] += ((len(encoding.encode(client.last_message)) / 1000) *  model_data["config"]["price_out"])

    
    print(st.session_state['main']['cost_in'])
    print(st.session_state['main']['cost_out'])
    print(st.session_state['main']['tokens_in'])
    print(st.session_state['main']['tokens_out'])

    return returnInfo

def add_objective(user_input: str, index: int = None):
    dprint(message="Adding objective: "+user_input)
    dprint(message="Index: "+str(index))
    st.session_state['exercise_objectives']['objectives'].append(user_input)
    if index != None:
        dprint(message="Removing suggestion: "+str(index))
        st.session_state['exercise_objectives']['suggestions'].pop(index)

def remove_objective(index: int):
    st.session_state['exercise_objectives']['suggestions'].append(st.session_state['exercise_objectives']['objectives'][index])
    st.session_state['exercise_objectives']['objectives'].pop(index)

# Streamlit page layout
st.set_page_config(page_title='ChatRange', layout='wide')

st.write(f"Session ID: {st.session_state['session']}")

# Create a header section with the background image
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

st.title('Exercise objectives')

# Create the column
col, buff, col2 = st.columns([2,1,2])


col.markdown(
    """
    The exercise objectives are the main goals of the exercise. They enable ChatRange to structure the exercise.
    """
    )

col.markdown(
    f"""
    If you want the suggestions to focus on specific topics, you can add them below. Or you can add your own learning objective by typing it in the text box below.
    """
    )

# Input content for objective focus
st.session_state['exercise_objectives']['tuning'] = col.text_area("Objective tuning", height=100, value=st.session_state['exercise_objectives']['tuning']) 

if col.button('Add focus'):
    st.session_state['exercise_objectives']['tuning'] = st.session_state['exercise_objectives']['tuning'].replace('\n', '  \n')
    col.write("Added")

# Add a manual objective
manual_input = col.text_input("Manual objective") 

if col.button('Add objective'):
    add_objective(manual_input)
    col.write("Added")

col.markdown("---")


# Run the scenario settings
if col.button('Get suggestions'):

    with st.spinner('Generating Objective suggestions...'):
        suggestions = get_ai_suggestion(
            focus=st.session_state['exercise_objectives']['tuning'],
            exercise_type=st.session_state['main']['type'],
            participants=st.session_state['main']['participants'],
            organization=st.session_state['main']['organization'],
            scenario=st.session_state['main']['scenario']
        )
        dprint(message="Suggestions: "+suggestions['last_message'], level=logging.DEBUG)
        #Load the json
        st.session_state['exercise_objectives']['suggestions'] = json.loads(str(suggestions['last_message']))

for suggestion in st.session_state['exercise_objectives']['suggestions']:
    col.write(f"{suggestion}")
    col.button("Add", on_click=add_objective, args=(suggestion, len(st.session_state['exercise_objectives']['objectives'])), type="primary", key=str(uuid.uuid4()) )


# Save to Redis
redis_client.set(f"{str(st.session_state['session'])}_exercise_objectives", str(json.dumps(st.session_state['exercise_objectives'])))
redis_client.close()

col2.header("Results")

def live_update_settings(status_placeholder):
    c = 0
    status_placeholder.markdown(f"""### Objectives""")
    status_placeholder.markdown(f"Click on the objective to remove it from the list")
    status_placeholder.markdown("---")

    

    for objective in st.session_state['exercise_objectives']['objectives']:
        status_placeholder.write(f"{objective}")
        status_placeholder.button("Remove", on_click=remove_objective, args=(c,), type="primary", key=str(uuid.uuid4()) )
        c += 1

live_update_settings(col2)


