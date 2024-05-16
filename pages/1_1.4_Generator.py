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

def create_objective(objectives: list):
    output = ""
    for objective in objectives:
        if output == "":
            output = objective
        else:
            output= output + dedent(f"""
                - {objective}""")
    return output
        

def get_parts(purpose: str, scenario: str):
    chat = OpenAIMessages()

    message = dedent(f"""
        Task: Decide if we should divide this exercise into multiple parts based on the Purpose and Scenario. The parts MUST only focus on the incident, not the response. Return the number of parts and a description for each part.

        Purpose: {purpose}
        Scenario: {scenario}

        Expexted output: Maximum two parts, divided logically by using the cyber kill chain.

        Notes: Only reply with the answer to the question and a title for the parts.
        """)
    
    dprint(message=message, level=logging.DEBUG)

    

    chat.add_message(content=message, role="user")

    json = False
    #Load the model data
    model_data = select_model(messages=chat, use="get_parts")
    client = model_data["model"]

    # Chat uintil we return a valid JSON
    errors = 0
    while True and errors < 1:
        return_id = False
        client.chat(return_id=return_id)

        if json == True:
            # Check if client.last_message is valid JSON
            if is_valid_json(client.last_message):
                return_id = client.chat_id
                chat.add_message(content="...", role="user")
                break

        errors += 1

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

    return client.last_message


def get_timeline(parts: str, scenario: str, threat_actor: str, company: str):
    chat = OpenAIMessages()

    message = dedent(f"""
        Task: Create a story timeline leading up yo the start point of the exercise scenario. Incorporate the target company, and the threat actor, into the story. use a formal and factual language for use in incident report.

        Description: The story must go over several days and there must be a clear progression of events that happen. The days must be in chronological order but there must be from 1 to 7 days between each day. Only write the day number as title title for the day.
        Only write the story up to the point where the first part of the exercise will begin.

        Create one story for each part. Each part must have at least four days in the timeline.
        
        Expexted Output: A timeline with a title for each day and a story for each day. Only write what is the expexted output.

        Company: {company}

        Parts: {parts}

        Scenario: {scenario}

        Threat Actor: {threat_actor}
        """)

    dprint(message=message, level=logging.DEBUG)
    
    #model_type = "gpt-3.5-turbo"
    #model_type="gpt-4-turbo-preview"

    chat.add_message(content=message, role="user")

    json = False
    #Load the model data
    model_data = select_model(messages=chat, use="get_timeline")
    client = model_data["model"]


    # Chat uintil we return a valid JSON
    errors = 0
    while True and errors < 1:
        return_id = False
        client.chat(return_id=return_id)

        if json == True:
            # Check if client.last_message is valid JSON
            if is_valid_json(client.last_message):
                return_id = client.chat_id
                chat.add_message(content="...", role="user")
                break

        errors += 1

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

    return client.last_message


def get_questions(objectives: list, parts: str, participants: str):
    chat = OpenAIMessages()

    message = dedent(f"""
        Task: Create questions for the participants of a cyber security tabletop exercise for each part of the exercise. The parts is provided.

        Description: All questions must mention the participant in the question.  Each question must have from 2 to 7 sub questions. The questions must be tailored to the expected participants level of knowledge based on their normal role in the organization. The questions must cover the objectives for the exercise as provided and must be written so they can be discussed among the participants. You must write at least seven main questions per part.

        Participants: {participants}
                     
        Example question:
        1.	Does your department or agency provide basic cybersecurity and/or information technology (IT) security awareness training to all users (including managers and senior executives)?
            * What does your training cover?
            * Is training required to obtain network access?


        Expected output: The title of the part and then all the questions and subquestions belonging to that part. Only write what is the expexted output.

        Objectives:
        {create_objective(objectives)}

        Parts:
        {parts}

        """)

    dprint(message=message, level=logging.DEBUG)
    
    #model_type = "gpt-3.5-turbo"
    #model_type="gpt-4-turbo-preview"

    chat.add_message(content=message, role="user")

    json = False

    #Load the model data
    model_data = select_model(messages=chat, use="get_questions")
    client = model_data["model"]

    # Chat uintil we return a valid JSON
    errors = 0
    while True and errors < 1:
        return_id = False
        client.chat(return_id=return_id)

        if json == True:
            # Check if client.last_message is valid JSON
            if is_valid_json(client.last_message):
                return_id = client.chat_id
                chat.add_message(content="...", role="user")
                break

        errors += 1

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

    return client.last_message


# Streamlit page layout
st.set_page_config(page_title='ChatRange', layout='wide')

st.write(f"Session ID: {st.session_state['session']}")

# Create a header section with the background image
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

st.title('Exercise Generation')
st.session_state['temp_out'] = ""

# Create the column
col, buff, col2 = st.columns([2,1,2])



col.markdown(
    """
    This page generates the whole exercise. Each generation is done in a step by step process with a feedback loop at the end of each step.
    """
    )

col.markdown(
    f"""
    Click the button bellow to enhance the exercise.
    """
    )

col.markdown("---")
if col.button('Create Parts'):
    with st.spinner('Creating text...'):
        dprint(message="Creating Parts", level=logging.INFO)
        st.session_state['generator']['parts'] = ""
        st.session_state['temp_out'] = get_parts(st.session_state['main']['purpose'], st.session_state['main']['scenario'])
        st.session_state['generator']['parts'] = st.session_state['temp_out']
        
# Run the Scenario enhancement
if col.button('Create Timeline'):
    with st.spinner('Creating text...'):
        st.session_state['generator']['timeline'] = ""
        st.session_state['temp_out'] = get_timeline(parts=st.session_state['generator']['parts'], scenario=st.session_state['main']['scenario'], threat_actor=st.session_state['threat_intel']['research'], company=st.session_state['main']['organization'])
        st.session_state['generator']['timeline'] = st.session_state['temp_out']


if col.button('Create Questions'):
    with st.spinner('Creating text...'):
        st.session_state['generator']['questions'] = ""
        st.session_state['temp_out'] = get_questions(objectives=st.session_state['exercise_objectives']['objectives'],parts=st.session_state['generator']['parts'],participants=st.session_state['main']['participants'])
        st.session_state['generator']['questions'] = st.session_state['temp_out']
    

# Save to Redis
redis_client.set(f"{str(st.session_state['session'])}_generator", str(json.dumps(st.session_state['generator'])))

redis_client.close()

col2.header("Result")

def live_update_settings(status_placeholder):
    status_placeholder.markdown(st.session_state['temp_out'])

live_update_settings(col2)


