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
            {"role": "system", "content": "Given a hard-to-understand receipt item, identify what it most likely is in as few words as possible."},
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    user_in = input("\nYou: ")
    while user_in not in ["", "exit", "quit"]:
        print("\nBot:", chat(user_in))
        user_in = input("\nYou: ")