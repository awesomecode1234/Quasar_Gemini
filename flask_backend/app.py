from  flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import os
import google.generativeai as genai
import pathlib

genai.configure(api_key="AIzaSyDelldPDFDHnMvJWGHqyzHApR1LiuPIMqY")
model = genai.GenerativeModel("gemini-1.5-flash")
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)    
        sample_pdf = genai.upload_file(file_path)
        response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
        return jsonify({'message': response.text}), 200
        
if __name__ == '__main__':
    app.run(debug=False)