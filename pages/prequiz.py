import streamlit as st 
import pandas as pd
import os

st.write(os.getcwd())
df = pd.read_csv("./LSATLR_questions.csv")
df['qid'] = df['qid'].astype(int)
prequiz_qs = df[df['qid'] < 0].sort_values(by='qid', ascending=False).reset_index(drop=True)

st.title("Pre-Quiz")
st.write("Please answer the following questions to the best of your ability. (Est. time: 15m)")

questions = []
for index, row in prequiz_qs.iterrows():
  st.write(f"Question {index + 1}:")
  questions.append(st.radio(
    row['Question'],
    [row['A'], row['B'], row['C'], row['D'], row['E']],
    key=f'prequiz{row["qid"]}',
  ))
  st.divider()

def on_submit():
  corr = []
  for index, row in prequiz_qs.iterrows():
    correct_answer = row[row['Correct Ans.']]
    if questions[index] == correct_answer:
      corr.append(1)
    else:
      corr.append(0)
  prequiz_qs['Correct'] = corr
  prequiz_qs.groupby('Subtopic').agg(num_correct=('Correct', 'sum'), num_questions=('Correct', 'count')).reset_index()
  st.session_state.prequiz_df = prequiz_qs
  
      

st.button("Submit", on_click=lambda: st.session_state.update({"prequiz_answers": questions}))
    
