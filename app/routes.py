from flask import jsonify, request, url_for, redirect, flash
from google.cloud import storage
from werkzeug.security import generate_password_hash
from app import app, db, User
import os


BUCKET_NAME = os.environ.get('BUCKET_NAME', 'gke-file-upload')

@app.route('/')
def index():
    return "Hello, World!"

# Route to upload a file to the bucket
@app.route('/upload-file', methods=['POST'])
def upload_blob_from_memory():
    """Uploads a file to the bucket."""
    file = request.files.get('file')
    if file:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return jsonify({'url': blob.public_url})
    return jsonify({'error': 'A File is required'}), 400
