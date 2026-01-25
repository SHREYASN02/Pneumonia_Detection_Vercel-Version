#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Killing Flask backend..."
    kill $FLASK_PID
}

# Trap the exit signal
trap cleanup EXIT

# Start the Flask backend
echo "Starting Flask backend..."
cd Frontend-code/Frontend-vscode
source env/bin/activate
python app.py &
FLASK_PID=$!
cd ../..

echo "Waiting for Flask backend to start..."
while ! nc -z localhost 5000; do
  sleep 0.1 # wait for 1/10 of a second before check again
done
echo "Flask backend started."

# Open the browser
echo "Opening application in browser..."
xdg-open http://127.0.0.1:5000 &

# Wait for the Flask process to exit
wait $FLASK_PID