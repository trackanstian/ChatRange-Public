import streamlit as st
import pandas as pd
import logging
from chatrange.helpers import dprint, conversation, format_string, nav_to

#If the UUID is not set then go to the Start
if 'main' not in st.session_state:
    nav_to("/1.0_Prompt_Engineering", st)

import logging
from chatrange.helpers import dprint, conversation, format_string, nav_to

# Streamlit page layout
st.set_page_config(page_title='ChatRange', layout='wide')

st.write(f"Session ID: {st.session_state['session']}")

# Create a header section with the background image
st.markdown('<div class="header"></div>', unsafe_allow_html=True)

st.title('Scenario overview')
st.markdown("This is the overview of your scenario. You can show the different parts that is currently set up for your scenario.")

tokens = round(st.session_state['main']['tokens_in'] + st.session_state['main']['tokens_out'], 5)
cost = round(st.session_state['main']['cost_in'] + st.session_state['main']['cost_out'], 5)

st.markdown("**Tokens Out**: "+str(st.session_state['main']['tokens_out']))
st.markdown("**Cost Out**: "+str(round(st.session_state['main']['cost_out'],8))+" $")

st.markdown("**Tokens In**: "+str(st.session_state['main']['tokens_in']))
st.markdown("**Cost In**: "+str(round(st.session_state['main']['cost_in'],8))+" $")


st.markdown("**Tokens**: "+str(tokens))
st.markdown("**Cost**: "+str(cost)+" $")


# Exercise objectives
st.header('Exercise objectives')
st.dataframe(pd.DataFrame(st.session_state['exercise_objectives']['objectives'], columns=['Objectives']), use_container_width=True)

