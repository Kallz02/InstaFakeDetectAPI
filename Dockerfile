# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y libuv1-dev zlib1g
# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose the port that the application will run on
EXPOSE 7860
EXPOSE 80
EXPOSE 443
EXPOSE 8080
EXPOSE 5000

# Use Gunicorn as the WSGI server
CMD ["python3","-m" ,"socketify" ,"app:app", "-w", "4", "-b", "0.0.0.0:7860"]
