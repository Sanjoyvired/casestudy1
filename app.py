from flask import Flask, request, jsonify
from PIL import Image
import cv2
import pytesseract
import os
import chatgpt
import translator
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'Documents'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['RESULT_FOLDER'] = 'Result'

# Update with your MongoDB URI
app.config['MONGO_URI'] = 'mongodb+srv://batch6:herovired@cluster0.aqifkg2.mongodb.net/legalTunna'
mongo = PyMongo(app)

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


@app.route('/create_request', methods=['POST'])
def create_request():
    data = request.get_json()

    # Verify if all required attributes are present in the request
    required_attributes = ['bank_name',
                           'branch_name', 'manager_name', 'due_date']
    if not all(attr in data for attr in required_attributes):
        return jsonify({'error': 'Incomplete request attributes'})

    # Extract attributes from the JSON data
    bank_name = data['bank_name']
    branch_name = data['branch_name']
    manager_name = data['manager_name']
    due_date = data['due_date']

    requests_collection = mongo.db.requests
    new_request = {
        'bank_name': bank_name,
        'branch_name': branch_name,
        'manager_name': manager_name,
        'due_date': due_date,
        'documents': [],
        'consolidated_result': ''
    }
    request_id = requests_collection.insert_one(new_request).inserted_id

    # Create a new file for the request
    file_path = os.path.join(
        app.config['RESULT_FOLDER'], f'{branch_name}_{str(request_id)}.txt')
    with open(file_path, 'w') as file:
        file.write('')

    return jsonify({'message': 'Request created successfully', 'request_id': str(request_id)})


@app.route('/process_documents/<request_id>', methods=['POST'])
def process_documents(request_id):
    requests_collection = mongo.db.requests
   # print(request_id)
    request_id = ObjectId(request_id)
    # keys = request.form.keys()
    # print(list(keys))
    request_doc = requests_collection.find_one(
        {'_id': request_id})
    if not request_doc:
        return jsonify({'error': 'Invalid request_id'})
    else:
        print("valid request id")

    if 'document' not in request.files:
        return jsonify({'error': 'No document found in the request'})
    print("checking document")

    document = request.files['document']
    print("checking Filename")
    if document.filename == '':
        return jsonify({'error': 'Empty filename'})

    if document and allowed_file(document.filename):
        filename = document.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        document.save(file_path)
        result_text = ocr_image(file_path, 'eng')
        result_text = chatgpt.formatter(result_text)

        # Append the result to the request's file
        branch_name = request_doc['branch_name']
        file_name = f'{branch_name}_{str(request_id)}.txt'
        file_path = os.path.join(app.config['RESULT_FOLDER'], file_name)
        with open(file_path, 'a') as file:
            file.write(result_text + '\n')

        processed_file = {
            'file_path': file_path,
            'output': result_text
        }
        requests_collection.update_one(
            {'_id': request_id},
            {'$push': {'documents': processed_file}}
        )

        updated_request = requests_collection.find_one({'_id': request_id})
        consolidated_result = ''.join(doc['output']
                                      for doc in updated_request['documents'])
        requests_collection.update_one(
            {'_id': request_id},
            {'$set': {'consolidated_result': consolidated_result}}
        )

    return jsonify({'message': 'Document processed successfully',
                    "content": updated_request})


@app.route('/get_request_data/<request_id>', methods=['GET'])
def get_request_data(request_id):
    # Retrieve the request from the database
    request_id = ObjectId(request_id)
    request_data = mongo.db.requests.find_one({'_id': request_id})

    if request_data:
        return jsonify(request_data["consolidated_result"])
    else:
        return jsonify({'error': 'Request not found'})

# Endpoint to get the list of requests


@app.route('/requests', methods=['GET'])
def get_requests():
    requests = mongo.db.requests.find(
        {}, {'_id': 1, 'bank_name': 1, 'manager_name': 1, 'due_date': 1, 'branch_name': 1})

    request_list = []
    for request in requests:
        request_list.append({
            'request_id': str(request['_id']),
            'bank_name': request['bank_name'],
            'manager_name': request['manager_name'],
            'due_date': request['due_date'],
            'branch_name': request['branch_name']
        })

    return jsonify(request_list)


@app.route('/get_Summary/<request_id>', methods=['GET'])
def get_Summary(request_id):
    # Retrieve the request from the database
    request_id = ObjectId(request_id)
    request_data = mongo.db.requests.find_one({'_id': request_id})
    consolidated_data = request_data["consolidated_result"]
    segments = consolidated_data.split("WHEREAS")
    flag = 0
    summary_text = "It appears from the deed and document under examination that"
    for index in segments:
        result = chatgpt.prompting(index)
        if (flag == 0):
            summary_text += "\n" + result
        elif (flag % 2 == 0):
            summary_text += "\n"+"After that" + result
        else:
            summary_text += "\n"+"Thereafter" + result
        flag = flag+1

    if request_data:
        # Update the request document with the summary
        mongo.db.requests.update_one(
            {'_id': request_id},
            {'$set': {'summary_text': summary_text}}
        )

        return jsonify({'summary_text': summary_text})
    else:
        return jsonify({'error': 'Request not found'})


if __name__ == '__main__':
    app.run()
