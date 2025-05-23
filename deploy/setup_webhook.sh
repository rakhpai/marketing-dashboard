#!/bin/bash
# Setup script for the webhook server
# This script installs the webhook server as a systemd service

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
REPO_PATH="/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing"
DEPLOY_DIR="$REPO_PATH/deploy"
SERVICE_NAME="marketing-webhook"
WEBHOOK_SECRET="$1"  # Pass the webhook secret as the first argument

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Check if webhook secret is provided
if [ -z "$WEBHOOK_SECRET" ]; then
    echo "Please provide a webhook secret as the first argument"
    echo "Usage: $0 <webhook_secret>"
    exit 1
fi

echo "Setting up webhook server..."

# Create deploy directory if it doesn't exist
mkdir -p "$DEPLOY_DIR"

# Make scripts executable
chmod +x "$DEPLOY_DIR/deploy.sh"
chmod +x "$DEPLOY_DIR/webhook_server.py"

# Update the webhook secret in the service file
sed -i "s/your_webhook_secret_here/$WEBHOOK_SECRET/g" "$DEPLOY_DIR/webhook.service"

# Copy the service file to systemd
cp "$DEPLOY_DIR/webhook.service" "/etc/systemd/system/$SERVICE_NAME.service"

# Reload systemd
systemctl daemon-reload

# Enable and start the service
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

# Check the status
systemctl status "$SERVICE_NAME"

echo "Webhook server setup complete!"
echo "The webhook server is now running on port 9876"
echo "Configure your GitHub webhook with the following settings:"
echo "  Payload URL: https://api.fgtwelve.ltd:9876/"
echo "  Content type: application/json"
echo "  Secret: $WEBHOOK_SECRET"
echo "  Events: Just the push event"
