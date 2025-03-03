FROM python:3.10-slim

# Install system packages required to build psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

WORKDIR /usr/local/app

# Copy + install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Install your package
RUN pip install --no-cache-dir -e .