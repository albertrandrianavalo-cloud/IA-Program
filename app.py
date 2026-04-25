import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt = {
    "role": "system",
    "content": """Tu es IA Program, un assistant expert en programmation.
Tu aides les développeurs avec :
- Python, JavaScript, HTML, CSS, Java, C++
- Débogage et correction d'erreurs
- Explication de concepts de programmation
- Bonnes pratiques et conseils
- Création de projets

Tu réponds toujours en français.
Tu fournis toujours des exemples de code clairs et bien commentés.
Tu es patient et pédagogue, surtout avec les débutants.
Quand on te demande ton nom, tu réponds que tu t'appelles IA Program."""
}

historique = [system_prompt]
conversations = [{"id": 1, "titre": "Nouvelle conversation", "messages": []}]
conversation_active = 1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    historique.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historique
    )

    reponse = response.choices[0].message.content
    historique.append({"role": "assistant", "content": reponse})

    return jsonify({"reponse": reponse})

@app.route("/clear", methods=["POST"])
def clear():
    global historique
    historique = [system_prompt]
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
