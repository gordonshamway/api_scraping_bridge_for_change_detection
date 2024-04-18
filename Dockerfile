# Use an official Python runtime as a parent image
FROM python:3.10.1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright
RUN playwright install

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV COMPOSER_EMAIL user@email.com
ENV COMPOSER_PASSWORD some_password

# Run app.py when the container launches
CMD ["python", "api.py"]