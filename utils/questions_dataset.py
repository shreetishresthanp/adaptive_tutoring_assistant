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

system_instruction = """You are an AI tutor that teaches users LSAT Logical Reasoning.
  Here is how your student performed on the practice quiz grouped by question type (num correct/num questions):
  Assumtion: (%d/%d)
  Find the flaw in the argument: (%d/%d)
  Inferece: (%d/%d)
  Justify the conclusion: (%d/%d)
  Method of reasoning: (%d/%d)
  Point at issue: (%d/%d)
  Role Play: (%d/%d)
  Strengthen: (%d/%d)
  Weaken the argument: (%d/%d)
  Based on this, classify them as Beginner / Intermediate / Advanced. Walk through the student on all topics, but focus on the ones they struggle with.
  Question the user to ensure that they understand the material.
  Use practice questions from the tool to ensure they understand the material.
  Never give a one word answer. Always keep the conversation moving.
  Once the user has studied all the topics, prompt them to press the next button. """