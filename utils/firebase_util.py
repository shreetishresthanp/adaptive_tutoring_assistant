import firebase_admin
from firebase_admin import credentials, db
import streamlit as st 

def init_connection():
  cred = credentials.Certificate('./cs6983-tutor-firebase-adminsdk-fbsvc-9db3bc9bd3.json')
  if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cs6983-tutor-default-rtdb.firebaseio.com/'
    })

def push_presurvey_data(q1, q2, q3, q3_other):
  ref = db.reference('presurvey')
  ref.push({
    'name': st.session_state.name,
    'group_id': st.session_state.group_id,
    'q1': q1,
    'q2': q2,
    'q3': q3,
    'q3_other': q3_other
  })

def push_postsurvey_data(q1, q2, q3, q4, q5, q6, q7, q8, q9):
  ref = db.reference('postsurvey')
  ref.push({
    'name': st.session_state.name,
    'group_id': st.session_state.group_id,
    'q1': q1,
    'q2': q2,
    'q3': q3,
    'q4': q4,
    'q5': q5,
    'q6': q6,
    'q7': q7,
    'q8': q8,
    'q9': q9
  })

def push_prequiz_data(prequiz_correct):
  ref = db.reference('prequiz')
  ref.push({
    'name': st.session_state.name,
    'group_id': st.session_state.group_id,
    'q1': prequiz_correct[0],
    'q2': prequiz_correct[1],
    'q3': prequiz_correct[2],
    'q4': prequiz_correct[3],
    'q5': prequiz_correct[4],
    'q6': prequiz_correct[5],
    'q7': prequiz_correct[6],
    'q8': prequiz_correct[7],
    'q9': prequiz_correct[8],
    'q10': prequiz_correct[9],
  })

def push_postquiz_data(postquiz_correct):
  ref = db.reference('postquiz')
  ref.push({
    'name': st.session_state.name,
    'group_id': st.session_state.group_id,
    'q1': postquiz_correct[0],
    'q2': postquiz_correct[1],
    'q3': postquiz_correct[2],
    'q4': postquiz_correct[3],
    'q5': postquiz_correct[4],
    'q6': postquiz_correct[5],
    'q7': postquiz_correct[6],
    'q8': postquiz_correct[7],
    'q9': postquiz_correct[8],
    'q10': postquiz_correct[9],
  })