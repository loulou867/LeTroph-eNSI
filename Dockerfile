# Use the official Python image as the base image
FROM python:3.11
RUN pip install --upgrade pip
# Install the application dependencies

# Define the entry point for the container
CMD ["python", "server.py"]
