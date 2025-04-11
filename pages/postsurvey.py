import streamlit as st 
from utils.firebase_util import push_postsurvey_data

st.title("Post-Survey")
st.write("Please answer the following questions")
q1 = st.radio("How was the difficulty of the second quiz compared to the first?",
              ["Easier", "Litttle Easier", "Similar", "Little Harder", "Harder"],
              key="postquiz1")
q2 = st.slider("On a scale of 1-5, how ready do you feel about your logical reasoning skills post the study?" \
               "1: No change at all\n" \
               "5: Significant improvement",
                1, 5, 3)
q3 = st.slider("How helpful did you find the AI tutor to help you learn concepts?" \
               "1: Not helpful at all\n" \
               "5: Extremely helpful",
                1, 5, 3)
q4 = st.slider("How often did you find it confusing and frustrating when learning?" \
                "1: Never" \
                "5: Frequently",
                1, 5, 3)
q5 = st.slider("How engaging did you find the tutoring experience?" \
               "1: Completely boring" \
               "5: Extremely engaging",
               1, 5, 3)
q6 = st.radio("Would you use this type of studing (textbook/AI) future learning experiences?",
              ["Yes", "No"],
              key="postquiz6")
q7 = st.text_input("What did you like about the learning experience?")
q8 = st.text_input("What did you dislike about the learning experience?")
q9 = st.text_input("What would you like to see improved in the future?")

btn = st.button("Submit")

if btn:
  push_postsurvey_data(q1, q2, q3, q4, q5, q6, q7, q8, q9)
  st.write("Thank you for your participation!")
  st.stop()