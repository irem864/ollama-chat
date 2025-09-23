import requests
import gradio as gr

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

def ask_ollama(prompt):
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if "response" in data:
            return data.get("response")
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0].get("content", str(data))
        return str(data)
    except Exception as e:
        return f"Error: {e}"

def chat_fn(user_message, history):
    history = history or []
    history.append(("You", user_message))
    full_prompt = "\n".join([f"{u}: {m}" for u, m in history] + ["Assistant:"])
    reply = ask_ollama(full_prompt)
    history.append(("Assistant", reply))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    state = gr.State([])
    txt = gr.Textbox(show_label=False, placeholder="Mesajınızı yazın ve Enter'a basın")
    txt.submit(chat_fn, [txt, state], [chatbot, state])
    demo.launch(server_name="0.0.0.0", server_port=7860)

