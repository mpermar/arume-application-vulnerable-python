# Use an official Python runtime as a parent image
FROM cgr.dev/chainguard/python

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Run Python script when the container launches
CMD ["python", "main.py"]
