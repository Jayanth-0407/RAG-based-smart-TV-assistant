from flask import render_template, request, jsonify, session
from groq import Groq
import os
import uuid
from dotenv import load_dotenv
from app import system_prompt

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))
conversations = {}

def get_history(sid):
    if sid not in conversations:
        conversations[sid] = []
    return conversations[sid]

@app.route("/")

def index():
    if "session_id" not in session:
        session["session_id"]=str(uuid.uuid4()) 
    return render_template("index.html")

@app.route("/chat", methods=["POST"])

def chat():
    data = request.get_json()
    user_msg = data.get("message","").strip()
    
    if not user_msg:
        return jsonify({"reply": "Please type something!"})

    sid=session.get("session_id", "default")
    history=get_history(sid)
    history.append({"role": "user", "content": user_msg})

    try:
        response=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + history,
            max_tokens=512,
        )
        reply=response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route("/reset", methods=["POST"])

def reset():
    sid=session.get("session_id", "default")
    conversations[sid]=[]
    return jsonify({"status": "ok"})