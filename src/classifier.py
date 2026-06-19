import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def classify_persona(user_message):

    prompt = f"""
You are a customer persona classifier.

Classify the user into exactly one category:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return ONLY valid JSON.

Format:
{{
    "persona": "",
    "confidence": 0.0
}}

User Message:
{user_message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except:
        return {
            "persona": "Unknown",
            "confidence": 0.0
        }


if __name__ == "__main__":

    msg = input("Enter message: ")

    result = classify_persona(msg)

    print("\nDetected Persona:")
    print(result["persona"])

    print("Confidence:")
    print(result["confidence"])