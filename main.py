from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import json
from google.cloud import vision
import os
import base64


app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Key.json'
client = vision.ImageAnnotatorClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.form.get('imageData')
    if image_data:
        # Strip the header from the data URL
        header, image_data = image_data.split(',', 1)
        # Convert to bytes
        image_bytes = base64.b64decode(image_data)
        image = vision.Image(content=image_bytes)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        return jsonify([label.description for label in labels])
    else:
        return 'No image data received.', 400


if __name__ == '__main__':
    app.run(debug=True)