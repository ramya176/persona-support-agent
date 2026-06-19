print("Classifier file is running")
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
    Classify the user into ONE category.

    Categories:
    1. Technical Expert
    2. Frustrated User
    3. Business Executive

    Return JSON format only.

    User Message:
    {user_message}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    msg = input("Enter message: ")

    result = classify_persona(msg)

    print(result)