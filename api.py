import os
import sys
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from util import base64_to_pil, hist_eq
from PIL import Image
from sql_utils import get_disease, get_user, register_user, update_user_count


app = Flask(__name__)

model = tf.keras.models.load_model('.\\mobilenet_v3')

def model_predict(img, model):
    img = img.resize((224, 224))

    img = hist_eq(img)

    x = image.img_to_array(img)

    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)

    print(preds)
    return preds

def detectDisease(img):
    preds = model_predict(img, model)

    pred_proba = "{:.3f}".format(np.amax(preds))
    print(pred_proba)

    result = str(classes[np.argmax(preds)])
    result = result.replace('_', ' ').capitalize()
    return result, pred_proba


classes = []

def getDiseaseProfile():
    print("todo")

with open('classes.txt') as f:
    lines = f.readlines()
    for i in lines:
        classes.append(i)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    response = get_user(username,password)
    return jsonify(result=response)

@app.route('/register', methods=['POST'])
def register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    register_user(username,password)

    return jsonify(result="OK")


@app.route('/updateCount', methods=['POST'])
def updateCount():
    username = request.get_json()['username']
    totalCount = request.get_json()['totalCount']
    update_user_count(username,totalCount)

    return jsonify(result="OK")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img = base64_to_pil(request.json)

    result, pred_proba = detectDisease(img)

    return jsonify(result=result, probability=pred_proba)

@app.route('/detect', methods=['POST'])
def detect():
    imgB64 = request.get_json()['image']

    img = base64_to_pil(imgB64)

    nick, pred_proba = detectDisease(img)
    print(nick)

    sqlResults = get_disease(nick.strip())

    name = sqlResults[0][0]
    description = sqlResults[0][1]
    image = sqlResults[0][2]

    return jsonify(result=nick, probability=pred_proba, name=name, description=description,image=image)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()