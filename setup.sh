#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Function to set up Python virtual environment
setup_venv() {
    # Check if venv directory exists
    if [ -d "venv" ]; then
        echo "Virtual environment already exists."
    else
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Virtual environment created."
    fi

    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate

    # Optional: Upgrade pip
    # echo "Upgrading pip..."
    # pip install --upgrade pip

    # Install requirements
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping dependency installation."
    fi

    echo "✅ Done!"
}

# Run the function
setup_venv

