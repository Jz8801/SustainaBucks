from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from google.cloud import vision
import requests
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
    
    recyclable = ['plastic', 'glass', 'metal', 'tin', 'aluminium', 'wood', 'paper', 'paperboard', 'textile']
    
    response_label = client.label_detection(image=image)
    labels = response_label.label_annotations

    material_labels = [label.description for label in labels 
                       if any(material in label.description.lower() for material in recyclable)]
    
    if len(material_labels) == 0:
        material_labels = ['No Recyclable Detected']


    response_logo = client.logo_detection(image=image)
    logos = response_logo.logo_annotations

    results = {
        'labels': material_labels,
        'logos': [logo.description for logo in logos],
    }

    return render_template('uploadResults.html', labels=results['labels'], logos=results['logos'])

@app.route('/recycle', methods=['POST','GET'])
def recycle():
    user_location = get_location()
    print(user_location)
    return render_template('mapDirection.html')

def get_location():
    api_key = 'AIzaSyAYJgLH4_JT5GnC-AMTEg27is4-y2NTsCk'

    geolocation_data = {
        'considerIp': 'true',
    }

    response = requests.post(
        'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key,
        json=geolocation_data
    )

    if response.status_code == 200:
        location = response.json().get('location')
        return location
    else:
        return response.json().get('error'), response.status_code


@app.route('/dispose', methods=['POST','GET'])
def dispose():
    return render_template('dispose.html')

if __name__ == '__main__':
    app.run(debug=True)