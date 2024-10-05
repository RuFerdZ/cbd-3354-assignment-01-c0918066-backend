# Microservices Backend Application

This is a Flask application that allows users to upload files to Google Cloud Storage, manage user accounts, and interact with a PostgreSQL database.

## Features

- User registration and management
- File upload to Google Cloud Storage
- Display user information
- RESTful API endpoints for CRUD operations

## Requirements

Before running the application, ensure you have the following installed:

- Docker
- Python 3.11 (for local development)
- PostgreSQL (for local development)

## Environment Variables

The application requires several environment variables to be set for proper configuration. You can set them directly in your Docker run command or in a `.env` file if running locally.

### Required Environment Variables

- `DB_HOST`: Host of your PostgreSQL database (e.g., `<host>`)
- `DB_NAME`: Name of your PostgreSQL database (e.g., `<db-name>`)
- `DB_USER`: PostgreSQL database username (e.g., `<db-user>`)
- `DB_PASSWORD`: Password for your PostgreSQL database (e.g., `<db-password>`)
- `BUCKET_NAME`: Name of your Google Cloud Storage bucket (e.g., `<file-upload-bucket>`)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account key JSON file (e.g., `access_key.json`)

## Running the Application

To run the application in a Docker container, use the following command:

```bash
docker run --rm -p 5000:5000 --name backend-app \
  -e DB_HOST='34.66.221.204' \
  -e DB_NAME='assignment01' \
  -e DB_USER='c0918066' \
  -e DB_PASSWORD='Test1234' \
  -e BUCKET_NAME='gke-file-upload' \
  -e GOOGLE_APPLICATION_CREDENTIALS='access_key.json' \
  gcr.io/myfirstapp-72240/backend-app:latest
```

To run the application locally, use the following command:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_HOST='<host>'
export DB_NAME='<db-name>'
export DB_USER='<db-user>'
export DB_PASSWORD='<db-password>'
export BUCKET_NAME='<file-upload-bucket>'
export GOOGLE_APPLICATION_CREDENTIALS='<access_key.json>'
python app.py
```

## API Endpoints

The application provides the following API endpoints:

### 1. **POST /add-user**

- **Description**: Adds a new user to the database.
- **Request Body**:
    - **Content-Type**: `application/json`
    - **Example**:
      ```json
      {
          "name": "John Doe",
          "email": "john@example.com",
          "password": "securepassword",
          "phone_no": "1234567890"
      }
      ```
- **Response**:
    - **Success**:
      ```json
      {
          "message": "User added successfully"
      }
      ```
    - **Error**:
      ```json
      {
          "error": "Email already exists"
      }
      ```

### 2. **POST /upload-file**

- **Description**: Uploads a file to the Google Cloud Storage bucket.
- **Request Body**:
    - **Form Data**:
        - `file`: The file to upload.
- **Response**:
    - **Success**:
      ```json
      {
          "url": "https://storage.googleapis.com/bucket-name/filename"
      }
      ```
    - **Error**:
      ```json
      {
          "error": "A File is required"
      }
      ```

### 3. **GET /get-users**

- **Description**: Retrieves a list of all users.
- **Response**:
    - **Success**:
      ```json
      {
          "users": [
              {
                  "id": 1,
                  "name": "John Doe",
                  "email": "john@example.com",
                  "phone_no": "1234567890"
              },
              ...
          ]
      }
      ```

### 4. **GET /get-user/<user_id>**

- **Description**: Retrieves information for a specific user by their ID.
- **Response**:
    - **Success**:
      ```json
      {
          "id": 1,
          "name": "John Doe",
          "email": "john@example.com",
          "phone_no": "1234567890"
      }
      ```
    - **Error**:
      ```json
      {
          "error": "User not found"
      }
      ```

