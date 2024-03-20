# Use the official Python image as the base image
FROM python:3.8

# Install the application dependencies
RUN pip install socket

# Define the entry point for the container
CMD ["python", "server.py", "runserver"]
