#!/bin/bash

# Determine which Python executable to use
if command -v python &> /dev/null; then
    PYTHON_EXECUTABLE=python
elif command -v python3 &> /dev/null; then
    PYTHON_EXECUTABLE=python3
else
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Create a virtual environment
$PYTHON_EXECUTABLE -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Dependencies
$PYTHON_EXECUTABLE -m pip install -r requirements.txt

# Create a .env file for externalized variables
cp sample.env .env

# Run migrations
$PYTHON_EXECUTABLE manage.py migrate

# Run tests
$PYTHON_EXECUTABLE manage.py test

# Install data from the data fixtures
$PYTHON_EXECUTABLE manage.py loaddata data/users.json data/polls.json

echo "\nPlease continue with How to Run instructions in README.md"