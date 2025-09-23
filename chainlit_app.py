import requests
import chainlit as cl

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

def ask_ollama(prompt: str) -> str:
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if "response" in data:
            return data["response"]
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0].get("content", str(data))
        return str(data)
    except Exception as e:
        return f"Error: {e}"

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    reply = ask_ollama(user_input)
    await cl.Message(content=reply).send()

