# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/local/app

# Copy dependencies file
COPY requirements.txt ./

# Install dependencies as root
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY weather_etl ./weather_etl

# Set proper permissions for the app user
RUN groupadd -r app && useradd --no-log-init -r -g app app && \
    chown -R app:app /usr/local/app

# Switch to non-root user
USER app

# Expose port 5000 for API or web service
EXPOSE 5000

# Run the ETL script
CMD [ "python", "weather_etl/extract.py" ]
