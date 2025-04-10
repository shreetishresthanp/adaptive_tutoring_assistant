import time
import os
import joblib
import streamlit as st
from utils.conceptexcerpts import concept_excerpts
from utils.exampleexcerpts import example_excerpts
from google import genai

st.set_page_config(page_title="LSAT Control - Textbook Tutor", page_icon="📘")
st.title("📘 LSAT Logical Reasoning - Textbook Learning (Control)")

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/groupa')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar allows a list of past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )

    # Save new chats after a message has been sent to AI
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
    
# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []

choices = ["A", "B", "C", "D", "E"]

# Dropdown to select topic
topic = st.selectbox("Choose a topic to review:", list(concept_excerpts.keys()))

# Display Concept
st.subheader("Concept Overview")
st.markdown(concept_excerpts[topic])

# Display Question
st.subheader("Practice Question")
q = example_excerpts[topic]
st.write(q[0])
for i, choice in enumerate(choices):
    st.write(f"{i}). {choice}")

# Show answer
if st.checkbox("Show Answer"):
    st.success(f"Correct Answer: {q[1]}")

# Save to file
joblib.dump(
    st.session_state.messages,
    f'data/{st.session_state.chat_id}-st_messages',
)
joblib.dump(
    st.session_state.gemini_history,
    f'data/{st.session_state.chat_id}-gemini_messages',
)




