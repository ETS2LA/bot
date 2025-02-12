# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from the current directory into the container
COPY . .

# Expose the port that the server will listen on
EXPOSE 8000

# Set the command to run when the container starts
CMD ["python", "main.py"]