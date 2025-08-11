# Use an official Python runtime as a parent image
FROM cgr.dev/chainguard/python@sha256:17cd737bfcfd3fd8b7a32036dcbbf80ae9e85c503f0b46d755e31208a46a392f

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Run Python script when the container launches
CMD ["python", "main.py"]
