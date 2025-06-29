# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Flask will run on (Northflank will map this)
EXPOSE 8080

# Start the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
