# TODO/improvements:
#  - Clean up code: duplicate ENV  and WORKDIR statements, remove old comments
#  - Reduce image size: by cleaning up after installations and removing tmp files (`apt-get clean …`, `rm -rf $POETRY_CACHE_DIR`, ...)
#  - Add .dockerignore: reduce image size and avoid adding local or sensitive files.
#  - Change user after installations: add a non-root user and run the command with that, e.g. `USER appuser`
#  - Parameterize builds by adding ARG:  e.g. `ARG PYTHON_VERSION=3.11-slim`
#  - Add metadata: e.g. git hash as env var, to link back to code, helps traceability. Image tag for versioning.

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Define environment variable
ENV NAME World

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3

# System dependencies
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/


# Project initialization
RUN poetry config virtualenvs.create false \
    &&  poetry install --no-interaction --no-ansi


# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
#CMD ["poetry", "run", "python", "app.py"]
CMD ["python", "src/serving/app.py"]