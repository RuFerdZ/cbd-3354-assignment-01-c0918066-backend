from flask import jsonify, request, url_for, redirect, flash
from google.cloud import storage
from werkzeug.security import generate_password_hash
from app import app, db, User, Message
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
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone_no = data.get('phone_no')

    if not name or not email or not password or not phone_no:
        return jsonify({'error': 'Please provide name, email, phone_no and password'}), 400

    # check if phone_no has 10 characters
    if len(phone_no) != 10:
        return jsonify({'error': 'Phone number should have 10 characters'}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    # Add new user
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password, phone_no=phone_no)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})


# Route to display all users
@app.route('/get-users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({'id': user.id, 'name': user.name, 'email': user.email, 'phone_no': user.phone_no})
    return jsonify({'users': users_list})


# Route to display user information by ID
@app.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'phone_no': user.phone_no})


# Route to update user information by ID
@app.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_no = data.get('phone_no')

    if not name or not email or not phone_no:
        return jsonify({'error': 'Please provide name, email and phone_no'}), 400

    # check if phone_no has 10 characters
    if len(phone_no) != 10:
        return jsonify({'error': 'Phone number should have 10 characters'}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != user_id:
        return jsonify({'error': 'Email already exists'}), 400

    user.name = name
    user.email = email
    user.phone_no = phone_no
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


# Route to delete user by ID
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


# Route to get all messages
@app.route('/get-messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    messages_list = []
    for message in messages:
        messages_list.append({'id': message.id, 'message': message.message, 'timestamp': message.timestamp})
    return jsonify({'messages': messages_list})
