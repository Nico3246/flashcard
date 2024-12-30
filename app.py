from flask import Flask, render_template, request, jsonify
import random
from google.cloud import firestore
import os
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)

# Configura Firebase

cred = credentials.Certificate('path_to_your_firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Inicializa la base de datos Firestore
db = firestore.Client()
flashcards_ref = db.collection('flashcards')

# Función para cargar las tarjetas desde Firestore
def load_flashcards():
    cards = flashcards_ref.stream()
    return [{'front': card.id, 'back': card.to_dict().get('back')} for card in cards]

# Función para guardar una nueva tarjeta en Firestore
def save_flashcard(front, back):
    flashcards_ref.document(front).set({'back': back})

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
