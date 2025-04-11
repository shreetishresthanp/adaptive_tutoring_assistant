import streamlit as st
from utils.conceptexcerpts import concept_excerpts
from utils.exampleexcerpts import example_excerpts
from utils.misc import end_session, display_pre_quiz

st.set_page_config(page_title="LSAT Group B", page_icon="📘")
st.title("📘Logical Reasoning: Group B")

display_pre_quiz()

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


next_page = st.button("Click here to end session")

if next_page:
    st.switch_page("pages/postquiz.py")




