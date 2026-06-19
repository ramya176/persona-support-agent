import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_response(query, persona, retrieved_text):

    prompt = f"""
You are a customer support assistant.

Persona: {persona}

Knowledge Base:
{retrieved_text}

User Query:
{query}

Instructions:

Technical Expert:
- Detailed explanation
- Technical terms
- Troubleshooting steps

Frustrated User:
- Empathetic tone
- Simple language
- Reassuring

Business Executive:
- Concise
- Impact focused
- Resolution guidance

Answer only using the knowledge base.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text