# Step 1: Build the image
FROM python:3.11-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the requirements file
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the source code
COPY . .

# Step 6: Expose the port
EXPOSE 5000

# Step 7: Run the application
CMD [ "python", "app.py" ]
