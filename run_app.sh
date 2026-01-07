#!/bin/bash

# News Aggregator Launcher Script

echo "Starting The Daily Digest News Aggregator..."
echo ""

# Check if running in headless environment
if [ -z "$DISPLAY" ]; then
    echo "No display detected. Starting virtual display (Xvfb)..."
    Xvfb :99 -screen 0 1920x1080x24 &
    XVFB_PID=$!
    export DISPLAY=:99
    sleep 2
    echo "Virtual display started on :99"
fi

# Run the application
echo "Launching application..."
python news_aggregator.py

# Clean up Xvfb if we started it
if [ ! -z "$XVFB_PID" ]; then
    kill $XVFB_PID 2>/dev/null
fi
