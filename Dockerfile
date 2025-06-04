FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget unzip gnupg ca-certificates chromium chromium-driver && \
    pip install --no-cache-dir flask selenium gunicorn

# Set environment variable so Selenium can find Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Copy app files
WORKDIR /app
COPY . /app

# Run the app
CMD ["gunicorn", "--workers=1", "--threads=1", "--timeout=60", "app:app"]
