#!/bin/bash
# Comprehensive script to set up automatic deployment
# This script:
# 1. Generates a webhook secret
# 2. Updates the webhook server configuration with the secret
# 3. Creates a deployment script on the server
# 4. Sets up the webhook server on the server
# 5. Provides instructions for manual webhook setup in GitHub

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration - EDIT THESE VALUES
SERVER_USER="your_server_username"
SERVER_IP="your_server_ip"
SERVER_PATH="/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing"
REPO_OWNER="rakhpai"
REPO_NAME="marketing-dashboard"

# Generate webhook secret if it doesn't exist
if [ ! -f "webhook_secret.txt" ]; then
    echo "Generating webhook secret..."
    openssl rand -hex 20 > webhook_secret.txt
fi

WEBHOOK_SECRET=$(cat webhook_secret.txt)
echo "Using webhook secret: $WEBHOOK_SECRET"

# Update webhook server configuration with the secret
echo "Updating webhook server configuration..."
sed -i "s/your_webhook_secret_here/$WEBHOOK_SECRET/g" webhook.service

# Create deployment package
echo "Creating deployment package..."
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/deploy"
cp deploy.sh webhook_server.py webhook.service setup_webhook.sh "$TEMP_DIR/deploy/"
cp webhook_secret.txt "$TEMP_DIR/deploy/"
chmod +x "$TEMP_DIR/deploy/deploy.sh" "$TEMP_DIR/deploy/webhook_server.py" "$TEMP_DIR/deploy/setup_webhook.sh"

# Transfer files to server
echo "Transferring files to server..."
ssh "$SERVER_USER@$SERVER_IP" "mkdir -p $SERVER_PATH/deploy"
scp -r "$TEMP_DIR/deploy/"* "$SERVER_USER@$SERVER_IP:$SERVER_PATH/deploy/"

# Clean up temporary directory
rm -rf "$TEMP_DIR"

# Set up webhook server on the server
echo "Setting up webhook server on the server..."
ssh "$SERVER_USER@$SERVER_IP" "cd $SERVER_PATH/deploy && sudo ./setup_webhook.sh $WEBHOOK_SECRET"

# Provide instructions for webhook setup in GitHub
echo ""
echo "=== NEXT STEPS ==="
echo "1. Set up the webhook in GitHub:"
echo "   a. Go to https://github.com/$REPO_OWNER/$REPO_NAME/settings/hooks"
echo "   b. Click 'Add webhook'"
echo "   c. Set Payload URL to: http://$SERVER_IP:9000/"
echo "   d. Set Content type to: application/json"
echo "   e. Set Secret to: $WEBHOOK_SECRET"
echo "   f. Select 'Just the push event'"
echo "   g. Click 'Add webhook'"
echo ""
echo "2. Test the webhook:"
echo "   a. Make a small change to your repository"
echo "   b. Commit and push the change"
echo "   c. Check the server logs to see if the deployment was triggered:"
echo "      ssh $SERVER_USER@$SERVER_IP 'tail -f $SERVER_PATH/deploy/webhook.log'"
echo ""
echo "Setup complete!"
