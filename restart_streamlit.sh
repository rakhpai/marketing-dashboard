#!/bin/bash

# Kill any existing Streamlit process on port 9005
echo "Stopping existing Streamlit processes on port 9005..."
pkill -f "streamlit run app.py --server.port=9005"

# Wait a moment for process to stop
sleep 2

# Start the Streamlit application
echo "Starting Streamlit marketing dashboard..."
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing
nohup streamlit run app.py --server.port=9005 --server.baseUrlPath=/marketing --server.enableCORS=false --server.enableWebsocketCompression=true --server.headless=true --server.address=0.0.0.0 > streamlit.log 2>&1 &

# Wait a moment for process to start
sleep 3

# Check if the process is running
if pgrep -f "streamlit run app.py --server.port=9005" > /dev/null; then
    echo "Streamlit marketing dashboard started successfully"
    echo "PID: $(pgrep -f 'streamlit run app.py --server.port=9005')"
else
    echo "Failed to start Streamlit marketing dashboard"
    echo "Check streamlit.log for errors:"
    tail -20 streamlit.log
fi