import streamlit as st 
from utils.firebase_util import init_connection
init_connection()

st.title("LSATLR Study")

st.write("""Welcome to our Study! The guidelines are as follows:          
         1. We'll start with a short survey followed by a pre-quiz of LSAT Logical Reasoning questions          
         2. Then you'll be assigned to a learning session based on your group (A or B)          
         3. Use the "Click here when finished" to end session once you're done 
         4. You'll then be directed to a post-quiz to review concepts learnt       
         5. The study ends with a post survey to assess general experience         
         6. You're expected to complete steps 1 - 5 in one sitting 
""")
st.write("Welcome to our Study! Please enter your name and group ID to begin.")

name =st.text_input("Name")
group_id = st.radio("Group ID", ["A", "B"])

start_btn = st.button("Start")

if start_btn:
  st.session_state.name = name
  st.session_state.group_id = group_id
  st.switch_page("pages/presurvey.py")

