#!/bin/bash

# echo message
echo "Starting setup..."

# make environment variables
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please set your environment variables in .env file"
    exit 1
fi

# make venv
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

echo "Setup completed!"