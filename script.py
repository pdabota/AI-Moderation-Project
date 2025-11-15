import requests

API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "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"

SYSTEM_PROMPT = "You are a helpful, polite assistant."

BANNED = ["kill", "hack", "bomb"]

def violates(text):
    text = text.lower()
    return any(word in text for word in BANNED)

def redact(text):
    for word in BANNED:
        text = text.replace(word, "[REDACTED]")
    return text

user_prompt = input("Enter your prompt: ")

if violates(user_prompt):
    print("Your input violated the moderation policy.")
else:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=body).json()
    ai_answer = response["choices"][0]["message"]["content"]

    if violates(ai_answer):
        print("⚠️ AI output had unsafe content. Showing safe version:")
        print(redact(ai_answer))
    else:
        print("AI:", ai_answer)

