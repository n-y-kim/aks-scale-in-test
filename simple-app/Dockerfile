# Use Python 3.11 as the base image
FROM --platform=linux/amd64 python:3.11
# Set the working directory in the container
WORKDIR /app
# Copy the 'simple-app' directory contents into the container at /app
COPY simple-app/ ./
# Copy the 'k8s' directory contents into the container at /app/k8s with the same folder name
COPY ./k8s/ ./k8s/
# Install the dependencies
RUN pip install -r requirements.txt
# Run dummy_log.py when the container launches
CMD ["python", "-u", "app.py"]