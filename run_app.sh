#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Killing Flask backend..."
    kill "$FLASK_PID"
}

# Trap the exit signal
trap cleanup EXIT

echo "Starting Flask backend..."

# Check if virtual environment exists, if not, create and install dependencies
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Installing dependencies..."
    ./.venv/bin/pip install -r requirements.txt
fi

cd Frontend-code/
source ../.venv/bin/activate
python app.py &
FLASK_PID=$!
cd ..

echo "Waiting for Flask backend to start..."
while ! nc -z localhost 5000; do
  sleep 0.1 # wait for 1/10 of a second before check again
done
echo "Flask backend started."

# Open the browser
echo "Opening application in browser..."
xdg-open http://127.0.0.1:5000 &

# Wait for the Flask process to exit
wait "$FLASK_PID"