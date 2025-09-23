import requests
import streamlit as st

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

# Streamlit UI
st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("🤖 Ollama Chatbot (Streamlit)")
st.write("Gemma3-1b modeli ile sohbet edebilirsiniz.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Mesajınızı yazın:")

if st.button("Gönder") and user_input:
    reply = ask_ollama(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Assistant", reply))

# Sohbet geçmişini göster
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧑 {sender}:** {message}")
    else:
        st.markdown(f"**🤖 {sender}:** {message}")

