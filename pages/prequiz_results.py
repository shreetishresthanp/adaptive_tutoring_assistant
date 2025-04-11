import streamlit as st 
import pandas as pd
import time

df = pd.read_csv("./LSATLR_questions.csv")
df['qid'] = df['qid'].astype(int)
prequiz_qs = df[df['qid'] < 0].sort_values(by='qid', ascending=False).reset_index(drop=True)

st.title("Pre-Quiz")
st.write("Results:")

def response_to_idx(response, row):
  if response == row['A']:
    return 0
  elif response == row['B']:
    return 1
  elif response == row['C']:
    return 2
  elif response == row['D']:
    return 3
  elif response == row['E']:
    return 4

questions = []
for index, row in prequiz_qs.iterrows():
  check_or_x = '✅' if st.session_state.pre_quiz_correct[index] == 1 else '❌'
  st.write(f"Question {index + 1}: {check_or_x}")
  questions.append(st.radio(
    row['Question'],
    [row['A'], row['B'], row['C'], row['D'], row['E']],
    key=f'prequiz{row["qid"]}',
    index=response_to_idx(st.session_state.pre_quiz_answers[index], row),
    disabled=True
  ))
  st.divider()

btn = st.button("Click here when finished")

if btn:
  if st.session_state.group_id == "A":
    st.session_state.tutor_start_time = time.time()
    st.switch_page("pages/llm_tutor.py")
  else:
    st.session_state.textbook_start_time = time.time()
    st.switch_page("pages/textbook.py")