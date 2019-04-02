import os
from keras.models import load_model
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import cv2 
from PIL import Image

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS 

def clasificar_animal(fotoUrl):
    pass

def convert_to_array(img):
    im = cv2.imread(img)
    img = Image.fromarray(im, 'RGB')
    image = img.resize((50, 50))
    return np.array(image)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return """ 
            <!doctype html>
            <title>Imagen clasificada</title>
            <h1>Imagen clasificada</h1> 
            """
    return """
    <!doctype html>
    <title>Suba una imagen para clasificar</title>
    <h1>Suba una imagen para clasificar</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Subir>
    </form>
    """

def load_keras_model():
    """Load in the pre-trained model"""
    global model
    model = load_model('model/clasificador_animales.h5')    

if __name__ == "__main__":    
    load_keras_model()
    app.run(host="0.0.0.0", port=50000)
