# First Stage: Builder
FROM python:3.10-slim as builder

# Install system dependencies needed for building packages
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

WORKDIR /usr/local/app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Second Stage: Final, Minimal Image
FROM python:3.10-slim

WORKDIR /usr/local/app

# Copy only necessary runtime dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy application files
COPY . .

# Install your package (if needed)
RUN pip install --no-cache-dir -e .

CMD ["python", "your_app.py"]  # Change this to your actual entry point
