# Use an official, lightweight Python runtime blueprint
FROM python:3.11-slim

# Set internal systems working directory inside the container
WORKDIR /app

# Install native Linux system level dependencies for network requests
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency file first to maximize build caching performance
COPY requirements.txt .

# Install enterprise cloud dataset frameworks
RUN pip install --no-cache-dir -r requirements.txt

# Copy our raw data engineering script files into the container
COPY extract_flight_data.py .

# Create the standard landing paths for our mock automated data lake environment
RUN mkdir -p data_lake/landing_zone

# Set the active container instruction execution path
CMD ["python", "extract_flight_data.py"]
