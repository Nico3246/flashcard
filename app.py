import firebase_admin
from firebase_admin import credentials, firestore
import random
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Inicializar Firebase
cred = credentials.Certificate('config/flashcards-f2395-firebase-adminsdk-mw060-41d2f35eec.json')
firebase_admin.initialize_app(cred)

# Conectar a Firestore (base de datos de Firebase)
db = firestore.client()

# Función para cargar las tarjetas desde Firestore
def load_flashcards():
    flashcards_ref = db.collection('flashcards')
    docs = flashcards_ref.stream()
    return [{'front': doc.to_dict()['front'], 'back': doc.to_dict()['back']} for doc in docs]

# Función para guardar una nueva tarjeta en Firestore
def save_flashcard(front, back):
    flashcards_ref = db.collection('flashcards')
    flashcards_ref.add({'front': front, 'back': back})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]
        save_flashcard(front, back)
        return jsonify({"message": "Flashcard created successfully!"})
    return render_template("create.html")

@app.route("/practice")
def practice():
    flashcards = load_flashcards()
    if not flashcards:
        return render_template("practice.html", flashcard=None)
    random_card = random.choice(flashcards)
    return render_template("practice.html", flashcard=random_card)

@app.route("/view")
def view():
    flashcards = load_flashcards()
    return render_template("view.html", flashcards=flashcards)

if __name__ == "__main__":
    app.run(debug=True)
