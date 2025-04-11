import streamlit as st 
from utils.firebase_util import push_presurvey_data

st.title("Pre-Survey")
st.write("Please take this short survey:")
q1 = st.slider("On a scale of 1-5, how familiar are you with the LSAT Logical Reasoning section?\n" \
               "1: Never heard of it\n" \
               "3: Studied to some extent\n" \
               "5: Taken the LSAT before", 1, 5, 3)
q2 = st.slider("On a scale of 1-5, how confident are you in solving Logical Reasoning questions?\n" \
               "1: Not confident at all" \
               "5: I can ace all the questions", 1, 5, 3)
st.write("Which resources do you use to study?")
q3 = {
  "textbook": st.checkbox("Textbooks"),
  "online_courses": st.checkbox("Online courses"),
  "practice_tests": st.checkbox("Practice tests"),
  "ai_tools": st.checkbox("AI tools"),
  "other": st.checkbox("Other"),
}
q3_other = st.text_input("If you selected 'Other', please specify:", disabled=not q3["other"])
st.write("If you are done, press submit to move onto the next phase.")
submit_btn = st.button("Submit")

if submit_btn:
  push_presurvey_data(q1, q2, q3, q3_other)
  st.switch_page("pages/prequiz.py")