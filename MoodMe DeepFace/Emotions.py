import cv2
from deepface import DeepFace
import numpy as np
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
#app.config['\\UPLOADS']

#path = "face_imag.png"
#image = cv2.imread(path)

#analyze = DeepFace.analyze(image, actions=['emotion'])
#print(analyze)
#print(analyze['dominant_emotion'])

path = "None"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        global path
        picture = request.files["pic"]
        path = secure_filename(picture.filename)
        #path = "global"
        picture.save(path)
        if path == "None":
            return render_template("site.html")
            print("Path", path)
        else:
            return redirect(url_for("results"))

        #print(analyze)
        #print(analyze['dominant_emotion'])`z
    else:
        return render_template("site.html")

@app.route("/results", methods=["POST", "GET"])
def results():
    global path
    image = cv2.imread(path)
    print(path)
    analyze = DeepFace.analyze(path, actions=['emotion'])
    dominant = analyze['dominant_emotion']
    #print(analyze)
    #print(dominant)
    for item in analyze['emotion']:
        round(analyze['emotion'][item], 2)
    return render_template("results.html", path=path, pathtype = type(path), dominant=dominant,
                           emotions=analyze['emotion'])

@app.route('/<filename>')
def upload(filename):
    return send_from_directory("/", filename)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)

