#!/bin/bash
apt -y install python-is-python3 git python3.10-venv


# Step-by-step instructions on how to install the project

# Clone the repository
git clone https://github.com/trackanstian/ChatRange-Public.git

# Navigate to the project directory
cd ChatRange-Public

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create and edit .env file
cp env.example .env

