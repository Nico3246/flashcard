from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Archivo para almacenar las tarjetas
DATA_FILE = "data.json"

# Función para cargar tarjetas
def load_flashcards():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Función para guardar tarjetas
def save_flashcards(flashcards):
    with open(DATA_FILE, "w") as f:
        json.dump(flashcards, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]
        flashcards = load_flashcards()
        flashcards.append({"front": front, "back": back})
        save_flashcards(flashcards)
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
