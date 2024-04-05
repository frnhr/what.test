FROM python:3.12

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev postgresql-contrib

# Install poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy only the requirements files into the container
COPY pyproject.toml poetry.lock /app/

# install requirements
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy the rest of the project files into the container
COPY app /app/

# Run collectstatic to gather static files
RUN python manage_prodselect.py collectstatic --noinput

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your application
CMD ["gunicorn", "prodselect.wsgi:application", "--bind", "0.0.0.0:80"]
