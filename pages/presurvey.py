import streamlit as st 

st.write("Please take this short survey:")
q1 = st.slider("On a scale of 1-5, how familiar are you with the LSAT Logical Reasoning section?\n" \
               "1: Never heard of it\n" \
               "3: Studied to some extent\n" \
               "5: Taken the LSAT before", 1, 5, 3)
q2 = st.slider("On a scale of 1-5, how confident are you in solving Logical Reasoning questions?\n" \
               "1: Not confident at all" \
               "5: I can ace all the questions", 1, 5, 3)
q3 = st.multiselect("What resources do you usually use for studying?", 
                    ["Textbooks", "Online courses", "Practice tests", "Tutoring", "Other"],
                    help="Select all that apply. If you select 'Other', please specify in the text box below."
                    )
q3_other = st.text_input("If you selected 'Other', please specify:", disabled="Other" not in q3)
st.write("If you are done, press submit to move onto the next phase.")
submit_btn = st.button("Submit")

if submit_btn:
  #TODO: submit the survey data to the database
  st.switch_page("pages/prequiz.py")