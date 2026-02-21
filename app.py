from flask import Flask, render_template, request, jsonify, session
from groq import Groq
import uuid
import os
from dotenv import load_dotenv
from RAG.rag_retriever import get_context #rag_retriever is in RAG folder

load_dotenv()  # reads GROQ_API_KEY from .env file

app = Flask(__name__)
app.secret_key = "secret_key"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversations = {}

def get_history(sid):
    if sid not in conversations:
        conversations[sid] = []
    return conversations[sid]

@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please type something!"})

    sid = session.get("session_id", "default")
    history = get_history(sid)

    
    context = get_context(user_msg)

    system_prompt = f"""
    You are a helpful product manual assistant.
    Answer ONLY using the context below.
    If the answer is not found, say you don't know.
    while answering, translate 메뉴 to english.

    CONTEXT:
    {context}
    """

    history.append({"role": "user", "content": user_msg})

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[{"role":"system","content":system_prompt}] + history,
            max_tokens=512,
        )
        reply = response.choices[0].message.content

        history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Sorry, something went wrong: {str(e)}"})

@app.route("/reset", methods=["POST"])

def reset():
    sid = session.get("session_id", "default")
    conversations[sid] = []
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)