import streamlit as st
from utils.conceptexcerpts import concept_excerpts
from utils.exampleexcerpts import example_excerpts
import time
from utils.firebase_util import push_study_time_data

st.set_page_config(page_title="LSAT Group B", page_icon="📘")
st.title("📘Logical Reasoning: Group B")

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


next_page = st.button("Click here when finished")

if next_page:
    print(time.time())
    print(st.session_state.textbook_start_time)
    push_study_time_data(time.time() - st.session_state.textbook_start_time)
    st.switch_page("pages/postquiz.py")




