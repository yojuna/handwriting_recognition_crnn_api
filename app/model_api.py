import os
import numpy as np
import base64
from flask import Flask, render_template, request, Response
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
from tensorflow import keras
from tensorflow.keras import backend as K
import cv2

from utils import preprocess, num_to_label
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

def predict_text(img):
    # read image
    image = cv2.imdecode(img)
    # cv2.imshow("decoded", image)
    cv2.imwrite("./test_img.jpg", image)
    # preprocess
    image = preprocess(image)
    # predict image text
    pred = model.predict(image)
    # decode ctc 
    decoded = K.get_value(K.ctc_decode(pred, 
                                       input_length=np.ones(pred.shape[0])*pred.shape[1], 
                                       greedy=True)[0][0])
    predicted_text = num_to_label(decoded[0])
    print("======================")
    print(predicted_text)
    return predicted_text


# curl -d "data=abc1234" -X POST http://localhost:8888/predict
@app.route('/predict', methods=['POST'])
# @cross_origin()
def predict():
    content = request.form['data']

    # https://stackoverflow.com/questions/33521891/from-jpg-to-b64encode-to-cv2-imread
    img = np.fromstring(base64.b64decode(content[22:]), dtype=np.uint8)
    
    prediction = predict_text(img)

    resp = Response(str(prediction))
    # https://stackoverflow.com/questions/5584923/a-cors-post-request-works-from-plain-javascript-but-why-not-with-jquery
    # https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# # curl -d "data=abc1234" -X POST http://localhost:8888/predict
# @app.route('/predict', methods=['POST'])
# def predict():
#     content = request.form['data']

#     # https://stackoverflow.com/questions/33521891/from-jpg-to-b64encode-to-cv2-imread
#     img = np.fromstring(base64.b64decode(content[22:]), dtype=np.uint8)
#     character = cv2.imdecode(img, 0)

#     resized_character = cv2.resize(character, (28, 28)).astype('float32') / 255
#     number = model.predict_classes(resized_character.reshape((1, 784)))[0]

#     resp = Response(str(number))
#     # https://stackoverflow.com/questions/5584923/a-cors-post-request-works-from-plain-javascript-but-why-not-with-jquery
#     # https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp


# # curl -d "data=abc1234" -X POST http://localhost:8888/sample_post
# @app.route('/sample_post', methods=['POST'])
# def sample_post():
#     content = request.form['data']
#     return content


# # curl http://localhost:8888
# @app.route('/')
# def hello_world():
#     character = cv2.imread('3.png', 0)
#     resized_character = cv2.resize(character, (28, 28)).astype('float32') / 255
#     number = model.predict_classes(resized_character.reshape((1, 28 * 28)))[0]

#     resp = Response(str(number))
#     # https://stackoverflow.com/questions/5584923/a-cors-post-request-works-from-plain-javascript-but-why-not-with-jquery
#     # https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp


if __name__ == '__main__':
    print("** Loading Model...")
    saved_model_dir = "../saved_model/model.h5"
    model = keras.models.load_model(saved_model_dir)
    print("** Model loaded")
    app.run(debug=True, port=8888)  