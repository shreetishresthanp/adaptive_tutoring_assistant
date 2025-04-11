import streamlit as st 
import pandas as pd
from utils.firebase_util import push_postquiz_data
import time

df = pd.read_csv("./LSATLR_questions.csv")
df['qid'] = df['qid'].astype(int)
postquiz_qs = df[df['qid'] > 0].sort_values(by='qid', ascending=True).reset_index(drop=True)

st.title("Post-Quiz")
st.write("Please answer the following questions to the best of your ability. (Est. time: 15m)")

questions = []
for index, row in postquiz_qs.iterrows():
  st.write(f"Question {index + 1}:")
  questions.append(st.radio(
    row['Question'],
    [row['A'], row['B'], row['C'], row['D'], row['E']],
    key=f'prequiz{row["qid"]}',
  ))
  st.divider()

def on_submit():
  duration = time.time() - st.session_state.postquiz_start_time
  corr = []
  for index, row in postquiz_qs.iterrows():
    correct_answer = row[row['Correct Ans.']]
    if questions[index] == correct_answer:
      corr.append(1)
    else:
      corr.append(0)
  postquiz_qs['Correct'] = corr
  postquiz_qs.groupby('Subtopic').agg(num_correct=('Correct', 'sum'), num_questions=('Correct', 'count')).reset_index()
  push_postquiz_data(corr, duration)
  st.switch_page("pages/postsurvey.py")
  
      

btn = st.button("Submit")
  
if btn:
  on_submit()


st.session_state.postquiz_start_time = time.time()