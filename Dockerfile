# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y wget gnupg ca-certificates fonts-liberation libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libdrm2 libgbm1 libxcomposite1 libxdamage1 libxrandr2 libpangocairo-1.0-0 libpango-1.0-0 libxext6 libxfixes3 --no-install-recommends &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser
RUN playwright install chromium

# Expose the app port
EXPOSE 10000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
