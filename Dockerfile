# Use a Python base image
FROM python:3.9-slim

# Set environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to utilize Docker cache
COPY requirements.txt /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask application files into the container
COPY . /app/

# Expose the port Flask will run on (default is 5000)
EXPOSE 5000

# Set the environment variable for Flask to run in production
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Start Flask in production mode
CMD ["flask", "run"]
