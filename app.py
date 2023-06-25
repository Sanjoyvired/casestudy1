from flask import Flask, request, jsonify
from PIL import Image
import cv2
import pytesseract
import os
import chatgpt
import translator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Documents'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Function to check if the file extension is allowed


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']

# Function to perform OCR on an image given its file path


def ocr_image(image_path, language):
    image = Image.open(image_path)
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(image, lang=language)
    return text


def fileWrite(data):
    print("writing into the File")
    print(data)
    fs = open("Result/file.txt", "a")
    fs.write(data)
    fs.close()


@app.route('/process_documents/ocr', methods=['POST'])
def process_documents():
    if 'documents' not in request.files:
        return jsonify({'error': 'No documents found in the request'})

    documents = request.files.getlist('documents')
    language = request.form.get('language', 'eng')

    consolidated_result = ""

    for document in documents:
        if document.filename == '':
            return jsonify({'error': 'Empty filename'})

        if document and allowed_file(document.filename):
            filename = document.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            document.save(file_path)
            result_text = ocr_image(file_path, language)
            result_text = chatgpt.formatter(result_text)
            fileWrite(result_text)

           # print(result_text)
            consolidated_result += result_text

    # final_output = consolidated_result

    if language != "eng":
        consolidated_result = translator.translatorWrapper(consolidated_result)

    print(consolidated_result)
    # final_output = chatgpt.prompting(consolidated_result)
    response = {
        'consolidated_result': consolidated_result
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
