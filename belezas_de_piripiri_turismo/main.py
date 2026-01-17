from flask import Flask, render_template, abort, jsonify, url_for, session, request, json, redirect

from init_firebase import init
from download_from_firestore import import_firestore
from upload_to_firestore import upload_to_firestore


app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.secret_key = "123"

# ===================== DADOS =====================
with open("exemplo.json", "r", encoding="utf-8") as f:
    CATEGORIAS = json.load(f)

# ===================== ROTAS =====================
@app.route("/import-data")
def import_data():
    return import_firestore()

@app.route("/export-data")
def export_data():
    return upload_to_firestore()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/categoria/<nome>")
def categoria(nome):
    lugares = CATEGORIAS.get(nome)

    if lugares is None:
        abort(404)

    return render_template(f"{nome}.html", lugares=lugares)


@app.route("/lugares/<int:id>")
def lugar(id):
    for lista in CATEGORIAS.values():
        for l in lista:
            if l["id"] == id:
                return render_template("detalhes.html", lugar=l)

    abort(404)


@app.route("/contato")
def contato():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
