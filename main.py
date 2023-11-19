from flask import Flask, render_template, request, session, url_for, redirect, jsonify
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
    image_data_webcam = request.form.get('imageData')
    image_data_upload = request.files.get('file')
    
    if image_data_webcam:
        # Strip the header from the data URL
        header, image_data = image_data_webcam.split(',', 1)
        # Convert to bytes
        image_bytes = base64.b64decode(image_data)
        image = vision.Image(content=image_bytes)
        # response = client.label_detection(image=image)
        # labels = response.label_annotations
        # return jsonify([label.description for label in labels])
    elif image_data_upload:
        content = image_data_upload.read()
        image = vision.Image(content=content)
        # response = client.label_detection(image=image)
        # labels = response.label_annotations
        # return jsonify([label.description for label in labels])
    else:
        return 'No image data received.', 400
    
    response_label = client.label_detection(image=image)
    labels = response_label.label_annotations

    response_logo = client.logo_detection(image=image)
    logos = response_logo.logo_annotations

    response_text = client.text_detection(image=image)
    texts = response_text.text_annotations

    results = {
        'labels': [label.description for label in labels],
        'logos': [logo.description for logo in logos],
        'text': [text.description for text in texts]
    }

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)