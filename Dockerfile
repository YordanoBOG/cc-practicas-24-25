# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gcc
#RUN apt-get install gcc
RUN pip install --no-cache-dir -r api/requirements.txt
RUN dpkg -i api/bvbrc-cli-1.040.deb || apt-get update && apt-get install -f -y

# Expose the desired port
EXPOSE 8000

# Run the application
CMD ["python3", "app.py"]
