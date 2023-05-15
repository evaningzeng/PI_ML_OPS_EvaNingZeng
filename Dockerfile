# Base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files to the working directory
COPY . .

# Expose the port your application will be running on
EXPOSE 8000

# Set the entry point to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
