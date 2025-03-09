# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /event-hub-backend

# Copy the current directory contents into the container at /api
COPY . /event-hub-backend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/event-hub-backend/src

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run wsgi.py when the container launches
CMD ["python", "wsgi.py"]
