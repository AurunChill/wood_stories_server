# Use the official Python image from the Docker Hub
FROM python:3.10

# Create and set the working directory
WORKDIR /usr/src/app

# Copy the requirements file first, for better caching of dependencies
COPY requirements.txt .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy the entire content of the local directory to the container
COPY . .

# Specify the command to run the app on container startup
CMD ["python", "main.py"]
