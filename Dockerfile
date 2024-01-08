# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the 'app' directory contents into the container at /app
COPY app/ ./

# Run dummy_log.py when the container launches
CMD ["python", "-u", "dummy_log.py"]