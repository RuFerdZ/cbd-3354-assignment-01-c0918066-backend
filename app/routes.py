from flask import jsonify, request, render_template, url_for, redirect, flash
from google.cloud import storage

from werkzeug.security import generate_password_hash
from app import app
import os


BUCKET_NAME = os.environ.get('BUCKET_NAME')

@app.route('/')
def index():
    return "Hello, World!"
