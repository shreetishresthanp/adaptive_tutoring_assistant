import streamlit as st 
import pandas as pd
from utils.firebase_util import push_prequiz_data
import time

df = pd.read_csv("./LSATLR_questions.csv")
df['qid'] = df['qid'].astype(int)
prequiz_qs = df[df['qid'] < 0].sort_values(by='qid', ascending=False).reset_index(drop=True)

st.title("Pre-Quiz")
st.write("Please answer the following questions to the best of your ability.\n\nFeel free to use a piece of scrap paper if it would help.\n\n(Est. time: 10-15m)")

questions = []
for index, row in prequiz_qs.iterrows():
  st.write(f"Question {index + 1}:")
  questions.append(st.radio(
    row['Question'],
    [row['A'], row['B'], row['C'], row['D'], row['E']],
    key=f'prequiz{row["qid"]}'
  ))
  st.divider()

def on_submit():
  print(time.time())
  print(st.session_state.prequiz_start_time)
  duration = time.time() - st.session_state.prequiz_start_time
  st.session_state.pre_quiz_answers = questions
  corr = []
  for index, row in prequiz_qs.iterrows():
    correct_answer = row[row['Correct Ans.']]
    if questions[index] == correct_answer:
      corr.append(1)
    else:
      corr.append(0)
  st.session_state.pre_quiz_correct = corr
  prequiz_qs['Correct'] = corr
  pqq_processed = prequiz_qs.groupby('Subtopic').agg(num_correct=('Correct', 'sum'), num_questions=('Correct', 'count')).reset_index()
  st.session_state.prequiz_df = pqq_processed
  push_prequiz_data(corr, duration)
  st.switch_page("pages/prequiz_results.py")
  
      

btn = st.button("Submit")
if btn:
  on_submit()

st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)