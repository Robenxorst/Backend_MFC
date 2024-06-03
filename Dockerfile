# Use the official Python image as base
FROM python:3.9-slim

# Set environment variables for database connection
ENV DB_NAME=mfc \
    DB_USER=postgres \
    DB_PASSWORD=1212 \
    DB_HOST=postgres \
    DB_PORT=5432

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the FastAPI server
CMD ["python3", "main.py"]