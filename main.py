from flask import Flask, render_template, request, jsonify
import cv2
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import easyocr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    image_data = file.read()
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    # image = 

    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(image)
    
    for detection in result:
        top_left = tuple(map(int, detection[0][0]))
        bottom_right = tuple(map(int, detection[0][2]))
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        image = cv2.putText(image, text, top_left, font, 0.5, (255, 0, 0), 2)

    # Convert the processed image to base64 for display
    _, buffer = cv2.imencode('.png', image)
    print(_)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return render_template('index.html', image_data=image_base64)



if __name__ == '__main__':
    app.run(debug=True)
