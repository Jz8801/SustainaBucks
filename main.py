from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import json
from google.cloud import vision
import os


app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Key.json'
client = vision.ImageAnnotatorClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    print("upload route reached")
    file = request.files.get('file')
    if not file:
        return 'No file uploaded.', 400
    
    content = file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return jsonify([label.description for label in labels])

if __name__ == '__main__':
    app.run(debug=True)