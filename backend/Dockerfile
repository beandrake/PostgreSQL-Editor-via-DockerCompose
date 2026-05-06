# Set base image (hose OS)
FROM python:3.13.9-alpine

# Set the working directory in the container.
WORKDIR /code

# Copy dependencies file to the working directory.
COPY requirements.txt .

# Install dependencies.
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# Makes this container's port available to other containers
EXPOSE 5000

# Command to run on the container when it starts
#CMD [ "python", "./app.py" ]
#CMD [ "python", "-m", "flask", "run" ]
CMD ["flask", "run", "-h", "0.0.0.0"]