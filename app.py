from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
from binary_HarmoMed import processing_img 

# /webapp
# |-- app.py           (Flask backend)
# |-- binary_HarmoMed.py
# |-- static/
# |   |-- uploads/
# |   |-- results/
# |   |-- css/
# |       |-- styles.css
# |-- templates/
# |   |-- index.html

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        reference_file = request.files['reference']
        target_file = request.files['target']

        ref_path = os.path.join(app.config['UPLOAD_FOLDER'], reference_file.filename)
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_file.filename)

        reference_file.save(ref_path)
        target_file.save(target_path)

        processing_img(ref_path, target_path)

        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():

    # ส่งพาธรูปผลลัพธ์ไปแสดงใน result page
    images = [
        'true_corrected_img_rgb1.jpg',
        'result_plot.jpg'
    ]
    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
