import streamlit as st
from os import path
import pymupdf  

st.set_page_config(page_title="LSAT Control - Textbook Tutor", page_icon="📘")
st.title("📘 LSAT Logical Reasoning - Group A")

# Upload the textbook PDF
pdf_file = path.abspath("utils/textbook.pdf")
if pdf_file:
    doc = pymupdf.open(pdf_file, filetype="pdf")

    # Topic selector
    topic_pages = {
        "The Basics of Logical Reasoning": [i for i in range(1,36)],
        "Must Be True": [i for i in range(66,92)],
        "Main Point Questions": [i for i in range(93,135)],
        "Conditional Reasoning": [i for i in range(136,191)],
        "Weaken Questions": [i for i in range(192,218)],
        "Cause and Effect Reasoning": [i for i in range(219,238)],
        "Strengthen, Justify, and Assumption": [i for i in range(239,309)],
        "Find the Flaw": [i for i in range(349,379)],
        "Evaluate the Argument": [i for i in range(429,439)],
    }
    
    topic = st.selectbox("Choose a topic:", list(topic_pages.keys()))
    pages = topic_pages[topic]

    # Extract and display text
    text = ""
    for p in pages:
        text += doc[p].get_text()

    st.subheader("📖 Concept Explanation")
    st.write(text)
