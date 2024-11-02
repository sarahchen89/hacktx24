from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("OPENAI_API_KEY")
if not key:
    raise ValueError("API key not found")

client = OpenAI(
    api_key=key,
)

def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "In a maximum of 3 words, decipher what the given receipt item is. Think about your answer carefully before you respond and try to use as little words as possible."},
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response.choices[0].message.content.strip()