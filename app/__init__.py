from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import secrets
import datetime
import threading
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

app = Flask(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'access_key.json'

CORS(app)  # Enable CORS for all routes

# Generate a secret key
secret_key = secrets.token_hex(16)  # 32 characters (16 bytes)

# Get from environment
DB_NAME = os.environ.get('DB_NAME', 'cbd3354')
USER = os.environ.get('DB_USER', 'cbd3354_usr')
PASSWORD = os.environ.get('DB_PASSWORD', 'cbd3354_pwd')
HOST = os.environ.get('DB_HOST', 'localhost')
PORT = '5432'

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone_no = db.Column(db.String(10), unique=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)


# Create the tables if they don't exist
with app.app_context():
    db.create_all()

# Google Cloud Pub/Sub setup
project_id = "myfirstapp-72240"
subscription_id = "backend-sub"
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def insert_message(message):
    with app.app_context():  # Ensure the app context is available
        try:
            new_message = Message(message=str(message), timestamp=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            db.session.add(new_message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback the session if there's an error
            print(f"Error inserting message: {e}")


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    message_data = message.data.decode("utf-8")
    print(f"Received message: {message_data}")
    insert_message(message_data)
    message.ack()  # Acknowledge the message only after processing


def start_subscriber():
    with subscriber:
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}..\n")
        try:
            # Keep listening indefinitely
            streaming_pull_future.result()
        except Exception as e:
            print(f"Subscriber error: {e}")


# Start the subscriber in a separate thread
subscriber_thread = threading.Thread(target=start_subscriber)
subscriber_thread.start()

# Import your routes
from app import routes

if __name__ == "__main__":
    app.run(debug=True)  # Set to False in production
