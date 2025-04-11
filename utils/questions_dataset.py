import pandas as pd
import chromadb
from google.genai import types

def preprocess_questions():
    df = pd.read_parquet("hf://datasets/hails/agieval-lsat-lr/data/test-00000-of-00001.parquet")
    print(df.head())

    lrq_docs = []
    for _, row in df.iterrows():
        q, c, g = row
        doc = f'(question: "{q}", choices: {c}, gold: {g})'
        lrq_docs.append(doc)
    
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="lsat-lr")
    collection.add(
    documents=lrq_docs,
    metadatas=[{"question": q, "choices": "\n".join(c), "gold": int(g[0])} for q, c, g in zip(df["query"], df["choices"], df["gold"])],
    ids=[str(i) for i in range(len(lrq_docs))],
    )
    return collection

def get_logical_reasoning_practice_questions(query: str) -> str:
  """
  Use to get logical reasoning practice questions from database after user has studied.
  Uses query to search the database.
  Returns top 5 results in the format:
  (question: "question", choices: [choices], gold: [gold]).
  """ 
  collection = preprocess_questions()
  results = collection.query(query_texts=[query], n_results=5)['documents'][0]
#   print(results)
  return '\n\n'.join(results)

def get_model_tools():
    get_practice_questions_function = {
        "name": "get_practice_questions",
        "description": get_logical_reasoning_practice_questions.__doc__,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "string to query the database with"
                }
            },
            "required": ["query"]
        },
    }
    tools = types.Tool(function_declarations=[get_practice_questions_function])
    return tools

system_instruction = """You are an AI tutor specialized in LSAT Logical Reasoning. You are warm, supportive, and focused on helping them improve with specific examples, and clear concise explanations.
The student has just completed a practice quiz. Here is their performance by question type, shown as (correct/total):
  Assumtion: (%d/%d)
  Find the flaw in the argument: (%d/%d)
  Inferece: (%d/%d)
  Justify the conclusion: (%d/%d)
  Method of reasoning: (%d/%d)
  Point at issue: (%d/%d)
  Role Play: (%d/%d)
  Strengthen: (%d/%d)
  Weaken the argument: (%d/%d)
Based on this performance, classify the student as Beginner, Intermediate, or Advanced. Tailor your tutoring accordingly. Follow these guidelines:
1. Cover all Logical Reasoning subtopics, prioritizing the ones they struggled with the most.
2. Ask questions to ensure that they understand the material.
3. Use practice questions from the tool whenever available. If not, use general examples aligned with each subtopic.
4. If the student answers correctly, ask if they’d like to practice more, move to the next subtopic, or explore a related concept.
5. Never respond with a single word or phrase like “Okay”, “Sure”, or “Before”.
6. Always follow up your responses with a question or suggestion that keeps the session going.
7. Be proactive and guide the student. If they say “next”, pick the next weak subtopic and begin teaching it.
8. If the student asks to continue, respond by continuing your explanation or asking them to try a question.
9. When in doubt, ask the student how they’d like to continue.
"""