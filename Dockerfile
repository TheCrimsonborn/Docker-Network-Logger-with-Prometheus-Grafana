# Use Python 3.12-slim for a lightweight Debian-based image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y tshark libpcap-dev iproute2 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY ./src/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the source code from `src/`
COPY ./src/network_logger.py /app/

# Create logs directory with correct permissions
RUN mkdir -p /logs && chmod 777 /logs

# Run the application
CMD ["python", "/app/network_logger.py"]
