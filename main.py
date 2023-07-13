from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
cors = CORS(app)

@app.route('/add_message', methods=['POST'])
def add_message():
    audio_file = request.files['audio']
    unique_prefix = str(uuid.uuid4())
    filename = unique_prefix + '_' + audio_file.filename
    audio_file.save(os.path.join('audio', filename))
    return jsonify({'filename': filename, 'message': 'Message added successfully.'})

@app.route('/list_messages', methods=['GET'])
def list_messages():
    files = os.listdir('audio')
    return jsonify({'messages': files})

@app.route('/delete_message/<filename>', methods=['DELETE'])
def delete_message(filename):
    file_path = os.path.join('audio', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'Message deleted successfully.'})
    else:
        return jsonify({'message': 'Message not found.'}), 404

if not os.path.exists('audio'):
    os.makedirs('audio')

if __name__ == '__main__':
    app.run()
