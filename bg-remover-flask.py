'''
Required packges to install CV, NumPy,Flask.
pip install opencv-python
pip install numpy
pip install Flask

after running this file open the following link the browerser 
http://127.0.0.1:5000/
after opennig the link upload the file 
the file save in the local 

'''


from flask import Flask, render_template_string, request
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FOLDER = 'output'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Processing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
        }
        input[type="file"] {
            display: none;
        }
        label {
            background-color: #3498db;
            color: #fff;
            padding: 10px;
            cursor: pointer;
        }
        input[type="range"] {
            width: 80%;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h2>Image Processing</h2>
    <form method="POST" enctype="multipart/form-data" action="/process">
        <label for="imageUpload">Upload Image</label>
        <input type="file" id="imageUpload" name="image">
        <br>
        <button type="submit">Process Image</button>
    </form>
</body>
</html>
''')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'Image not found.'

    image_file = request.files['image']
    if image_file.filename == '':
        return 'No selected file.'

    if image_file and allowed_file(image_file.filename):


        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_image.png')
        image_file.save(filename)
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 100]) 
        upper_white = np.array([255, 25 + 5, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)

    
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

     
        inverse_mask = cv2.bitwise_not(mask)
        result_no_background = cv2.bitwise_and(img, img, mask=inverse_mask)
        cv2.imwrite('output_image_web.png', result_no_background)
        os.remove(filename)

        return 'Image processed successfully!'

    return 'Invalid file format.'

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
