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
RUN playwright install-deps

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV COMPOSER_EMAIL user@email.com
ENV COMPOSER_PASSWORD some_password
ENV COMPOSER_TIMEOUT_SECONDS 10
ENV PV_EMAIL user@email.com
ENV PV_PASSWORD some_password
ENV PV_TIMEOUT_SECONDS 10

# Run app.py when the container launches
# CMD ["python", "api.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]