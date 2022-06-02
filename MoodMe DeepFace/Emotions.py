import cv2
from deepface import DeepFace
import numpy as np
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
path = "None"


@app.route("/", methods=["POST", "GET"])
def home():
    try:
        if request.method == "POST":
            global path
            picture = request.files["pic"]
            path = secure_filename(picture.filename)
            picture.save(path)
            if path == "None":
                return render_template("site.html")
            else:
                return redirect(url_for("results"))
    except:
        return render_template("site.html", error="Please enter a valid file type with a face")
    else:
        return render_template("site.html")


@app.route("/results", methods=["POST", "GET"])
def results():
    try:
        global path
        analyze = DeepFace.analyze(path, actions=['emotion'])
        dominant = analyze['dominant_emotion']
        for item in analyze['emotion']:
            round(analyze['emotion'][item], 2)
        remove_file()
        return render_template("results.html", path=path, dominant=dominant,
                               emotions=analyze['emotion'])
    except:
        remove_file()
        return render_template("site.html", error="Please enter a valid file type with a face")


def remove_file():
    defaults = ["Emotions.py", "global", "templates"]
    for filename in os.listdir():
        if filename not in defaults:
            print("remove", filename)
            os.remove(filename)


@app.route('/<filename>')
def upload(filename):
    return send_from_directory("/", filename)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
