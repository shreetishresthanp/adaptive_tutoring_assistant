import streamlit as st
from google import genai
from google.genai import types

# Show title and description.
st.title("💬 LSAT Tutor")
st.write(
    "Hey there! I'm your tutor for today. We'll revise the LSAT Logical Reasoning Section."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
GEMINI_API_KEY = "AIzaSyAjpHA08BUwLhK-tIlORxcB18RAp3541-M"

# Create a client.
client = genai.Client(api_key=GEMINI_API_KEY)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Ready to begin?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
      #   stream = client.chat.completions.create(
      #   model="gemini-2.0-flash",
      #   # config=types.GenerateContentConfig(
      #   # system_instruction=system_instruction,
      #   # tools=[tools]),
      #   messages=[
      #       {"role": m["role"], "content": m["content"]}
      #       for m in st.session_state.messages
      #   ],
      #   stream=True,
      # )

    stream = client.chats.create(model="gemini-2.0-flash",
        # messages = [
        #     {"role": m["role"], "content": m["content"]}
        #     for m in st.session_state.messages
        # ]
    # config=types.GenerateContentConfig(
    #   system_instruction=system_instruction,
    #   tools=[tools]
    # )
    )

        # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream.send_message(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})





# # Streamed response emulator
# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Hi there. Do you need help?",
#         ]
#     )
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)


