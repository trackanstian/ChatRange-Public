import json
import streamlit as st
from chatrange.redis import get_redis_client
#Start Redis
redis_client = get_redis_client()

def persist_state(sessions: list, session_id: str, session_state: dict):
    for session in sessions:
        st.session_state[session] = json.loads(redis_client.get(f"{str(st.session_state['main']['uuid'])}_{session}"))
    st.session_state['main']['uuid'] = session_id
    st.text(f"Loaded session {session_id}")
