import os
from pathlib import Path
from dotenv import load_dotenv

from groq import Groq

load_dotenv()

GROQ_MODEL = os.getenv('GROQ_MODEL')

DB_PATH = Path(__file__).resolve().parent / "db.sqlite"

client_small_talk = Groq()

SMALL_TALK_PROMPT = """You are a friendly e-commerce shopping assistant chatbot. You help customers find and buy shoes.

When users ask about you (your name, what you are, what you do, etc.), respond as a single unified assistant — never mention that you are made up of multiple models, routes, or components. You are one chatbot, not a pipeline.

Keep responses short, warm, and conversational. If a question falls outside your scope, gently steer the conversation back to how you can help with shopping.
"""

def small_talk_interaction(question):

    chat_completion = client_small_talk.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SMALL_TALK_PROMPT,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}",
            },
        ],
        model = GROQ_MODEL,
        temperature=0.2,
    )
    
    return chat_completion.choices[0].message.content 

if __name__ == "__main__":
    question1 = "How are you"
    question2 = "What is your name?"
    question3 = "What are you?"
    for q in [question1, question2, question3]:
        answer = small_talk_interaction(q)
        print(answer)
    # query = "SELECT * FROM product WHERE brand LIKE '%nike%'"
    # df = run_query(query)
    pass
