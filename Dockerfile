# Base Image
FROM python:3.8

# Our working directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# For documentation reasons
EXPOSE 5000

# Define environment variable
ENV NAME ProductService
ENV FLASK_APP app:create_app

# Run the flask application
CMD ["flask", "run", "--host", "0.0.0.0"]