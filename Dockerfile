# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
# This includes the app directory and other files at the project root
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the outside world from the container
EXPOSE 8000

# Define environment variable to specify the name of the Python file to run
ENV FLASK_APP=run.py

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

