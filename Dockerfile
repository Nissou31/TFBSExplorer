# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Labels for image metadata
LABEL maintainer="Anes AMRI <anes.devops.31@gmail.com>" \
    name="TFBS Explorer" \
    description="This project identifies cis-regulating TFBS of a set of genes using Biopython and FastAPI, with integration to NCBI and JASPAR databases." \
    version="1.0.0"


# Set environment variables to ensure that the Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
EXPOSE 80

# Run Nginx and the FastAPI app using supervisord
CMD ["sh", "-c", "uvicorn app.main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"]
