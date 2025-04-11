import time
import streamlit as st
from utils.questions_dataset import system_instruction, get_model_tools
from google.genai import types
from google import genai

st.set_page_config(page_title="LSAT Group A", page_icon="📘")

GEMINI_API_KEY = "AIzaSyAjpHA08BUwLhK-tIlORxcB18RAp3541-M"
client = genai.Client(api_key=GEMINI_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

st.title("📘Logical Reasoning: Group A")
next_btn = st.button("Click here when finished")

st.write("Use this AI Tutor to help you understand the concepts. You can ask it to explain the concepts, provide examples, or clarify any doubts you have.")
st.write("Start by sending a hello message!")

sys_prompt = system_instruction % (
    st.session_state.prequiz_df['num_correct'][0],
    st.session_state.prequiz_df['num_questions'][0],
    st.session_state.prequiz_df['num_correct'][1],
    st.session_state.prequiz_df['num_questions'][1],
    st.session_state.prequiz_df['num_correct'][2],
    st.session_state.prequiz_df['num_questions'][2],
    st.session_state.prequiz_df['num_correct'][3],
    st.session_state.prequiz_df['num_questions'][3],
    st.session_state.prequiz_df['num_correct'][4],
    st.session_state.prequiz_df['num_questions'][4],
    st.session_state.prequiz_df['num_correct'][5],
    st.session_state.prequiz_df['num_questions'][5],
    st.session_state.prequiz_df['num_correct'][6],
    st.session_state.prequiz_df['num_questions'][6],
    st.session_state.prequiz_df['num_correct'][7],
    st.session_state.prequiz_df['num_questions'][7],
    st.session_state.prequiz_df['num_correct'][8],
    st.session_state.prequiz_df['num_questions'][8]
) if st.session_state.prequiz_df is not None else ""

st.session_state.chat_id = new_chat_id
st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
st.session_state.gemini_history = []

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = None
    
    st.session_state.chat = client.chats.create(model='gemini-2.0-flash',
                                            config=types.GenerateContentConfig(
                                            tools=[get_model_tools()],
                                            system_instruction=sys_prompt),
                                            history=st.session_state.gemini_history 
                                            )
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['text'])

# Chat input
user_input = st.chat_input("💬 Ask your tutor a question...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})
    full_response = ""

    response = st.session_state.chat.send_message_stream(user_input)
    
    full_reply = ""
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
        ):
        response_box = st.empty()
        for chunk in response:
            chunk_text = chunk.text
            if chunk_text:
                full_reply += chunk_text
                time.sleep(0.05)
                response_box.markdown(full_reply + "▌")

    # Final display after stream ends
    response_box.markdown(full_reply)
    st.session_state.messages.append({"role": "assistant", "text": full_reply, "avatar": AI_AVATAR_ICON})

    st.session_state.gemini_history = st.session_state.chat.get_history()

if next_btn:
    st.switch_page("pages/postquiz.py")