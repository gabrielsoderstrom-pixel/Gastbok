from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)
FIL = "gastbok.json"


def las_inlagg():
    # Läser alla inlägg från filen. Om filen inte finns än får vi en tom lista.
    try:
        with open(FIL, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def spara_inlagg(inlagg):
    # Skriver alla inlägg till filen i JSON-format.
    with open(FIL, "w", encoding="utf-8") as f:
        json.dump(inlagg, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    inlagg = las_inlagg()
    inlagg.reverse()  # nyaste inlägget först
    return render_template("index.html", inlagg=inlagg)


@app.route("/skicka", methods=["POST"])
def skicka():
    nytt = {
        "name": request.form["name"],
        "email": request.form["email"],
        "homepage": request.form["homepage"],
        "comment": request.form["comment"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    inlagg = las_inlagg()
    inlagg.append(nytt)
    spara_inlagg(inlagg)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)