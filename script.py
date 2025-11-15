import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BANNED = ["kill", "bomb", "hack"]

def moderate(text):
    lower = text.lower()
    for bad in BANNED:
        if bad in lower:
            return False
    return True

def censor_output(text):
    result = text
    for bad in BANNED:
        result = result.replace(bad, "[REDACTED]")
    return result

while True:
    user_prompt = input("Enter your prompt (or type 'exit' to quit): ")

    if user_prompt.lower() == "exit":
        print("Goodbye!")
        break

    if not moderate(user_prompt):
        print("Your input violated the moderation policy.")
        continue

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a friendly helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers=headers
    )

    ai_message = response.json()["choices"][0]["message"]["content"]

    if not moderate(ai_message):
        print("Your output violated the moderation policy.")
    else:
        print("AI:", censor_output(ai_message))
