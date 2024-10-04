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


# Route to add a new user
@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if not name or not email or not password:
        return jsonify({'error': 'Please provide name, email and password'}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400
    
    # Add new user
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})
