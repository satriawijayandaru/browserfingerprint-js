# Use Python's official image as the base
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the application files into the container
COPY . /app

# Expose port for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
