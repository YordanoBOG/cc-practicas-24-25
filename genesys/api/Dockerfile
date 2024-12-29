# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /genesys_app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]