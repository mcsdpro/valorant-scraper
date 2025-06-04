#!/bin/bash

# Install Chromium and ChromeDriver
apt-get update
apt-get install -y chromium chromium-driver

# Run your app
gunicorn app:app
