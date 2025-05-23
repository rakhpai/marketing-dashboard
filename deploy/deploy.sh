#!/bin/bash
# Deployment script for marketing dashboard
# This script pulls the latest changes from the git repository
# and restarts any necessary services

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
REPO_PATH="/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing"
LOG_FILE="/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/deploy.log"
BRANCH="master"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create log directory if it doesn't exist
mkdir -p $(dirname "$LOG_FILE")

# Log function
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Change to repository directory
cd "$REPO_PATH"

# Log deployment start
log "Starting deployment..."

# Check if directory is a git repository
if [ ! -d ".git" ]; then
    log "Error: $REPO_PATH is not a git repository"
    exit 1
fi

# Save the current commit hash
OLD_COMMIT=$(git rev-parse HEAD)
log "Current commit: $OLD_COMMIT"

# Fetch the latest changes
log "Fetching latest changes..."
git fetch origin

# Check if there are any changes
if git diff --quiet "$OLD_COMMIT" "origin/$BRANCH"; then
    log "No changes detected. Skipping deployment."
    exit 0
fi

# Pull the latest changes
log "Pulling latest changes..."
git pull origin "$BRANCH"

# Get the new commit hash
NEW_COMMIT=$(git rev-parse HEAD)
log "New commit: $NEW_COMMIT"

# Check if requirements.txt has changed
if git diff --name-only "$OLD_COMMIT" "$NEW_COMMIT" | grep -q "requirements.txt"; then
    log "requirements.txt has changed. Updating dependencies..."
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    pip install -r requirements.txt
fi

# Check if we need to restart Streamlit
if git diff --name-only "$OLD_COMMIT" "$NEW_COMMIT" | grep -q "app.py\|src/"; then
    log "Application files have changed. Restarting Streamlit..."
    # Check if restart_streamlit.sh exists and is executable
    if [ -x "./restart_streamlit.sh" ]; then
        ./restart_streamlit.sh
    else
        log "Warning: restart_streamlit.sh not found or not executable"
        # Try to restart Streamlit manually
        pkill -f "streamlit run app.py" || true
        nohup streamlit run app.py > streamlit.log 2>&1 &
    fi
fi

# Log deployment completion
log "Deployment completed successfully!"
