# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
