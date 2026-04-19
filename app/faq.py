import os
from pathlib import Path
import uuid
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# constants
FAQ_PATH = Path(__file__).parent / "resources/faq_data.csv"
EMBEDDING_FUNCTION = 'sentence-transformers/all-MiniLM-L6-v2'
COLLECTION_NAME_FAQ = 'faqs'


# vector db
chroma_client = chromadb.Client()
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_FUNCTION)


# llm
groq_client = Groq(api_key=GROQ_API_KEY)


def ingest_faq_data(path):
    if COLLECTION_NAME_FAQ in [c.name for c in chroma_client.list_collections()]:
        print(f"Collection: {COLLECTION_NAME_FAQ} already exists!")
        return
    
    print("Ingesting data into chromaDB...")    
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME_FAQ,
        embedding_function=ef
    )
    
    df = pd.read_csv(path)
    
    docs = df['question'].to_list()
    metadata = [{'answer': ans } for ans in df['answer'].to_list()]
    ids = [str(uuid.uuid4()) for _ in docs]
    
    collection.add(
        documents=docs,
        metadatas=metadata,
        ids=ids
    )
    
def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=COLLECTION_NAME_FAQ)
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result
    
def faq_chain(query):
    qa = get_relevant_qa(query)
    
    context = ''.join([r['answer'] for r in qa['metadatas'][0]])
    
    prompt = f'''
        You are a chat assistant working for the company.
        Given the question and FAQ below, generate the answer based on the context only.. If you don't find the answer inside the context then say "I don't know". Do not make things up.

        QUESTION: {query}

        CONTEXT: {context}
    '''
    
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model = GROQ_MODEL,
    )
    
    return chat_completion.choices[0].message.content    
    

if __name__ == "__main__":
    ingest_faq_data(FAQ_PATH)
    query1 = 'Whats your policy on on defective products?'
    query2 = 'Do you take cash as a payment?'
    result = faq_chain(query2)
    print(result)