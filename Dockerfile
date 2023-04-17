# Base image
FROM python:3.8
# Working directory
WORKDIR /app
# Copy requirements file and install dependencies
RUN pip install -r requirements.txt
# Copy the rest of the project files
COPY ..
# Expose the server port
EXPOSE 8080
# Command to start the server
CMD ["python", "routes.py", "gunicorn", "-b", "0.0.0.0:8080", "blog:app"]
