#!/bin/bash
# Script to create a GitHub webhook using the GitHub API

# Configuration
REPO_OWNER="rakhpai"
REPO_NAME="marketing-dashboard"
WEBHOOK_URL="http://your-server-ip:9000/"
WEBHOOK_SECRET=$(cat webhook_secret.txt)
GITHUB_TOKEN=""  # You'll need to provide your GitHub token

# Check if GitHub token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Please provide your GitHub token by editing this script or setting the GITHUB_TOKEN environment variable"
    echo "You can create a token at https://github.com/settings/tokens"
    echo "The token needs the 'repo' scope"
    
    # Try to get token from environment
    if [ -n "$GITHUB_TOKEN_ENV" ]; then
        GITHUB_TOKEN="$GITHUB_TOKEN_ENV"
        echo "Using GitHub token from environment variable"
    else
        echo "No GitHub token found. Exiting."
        exit 1
    fi
fi

# Create the webhook
echo "Creating webhook for $REPO_OWNER/$REPO_NAME..."
echo "Webhook URL: $WEBHOOK_URL"
echo "Webhook Secret: $WEBHOOK_SECRET"

# Create the webhook using the GitHub API
response=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/hooks" \
  -d '{
    "name": "web",
    "active": true,
    "events": ["push"],
    "config": {
      "url": "'"$WEBHOOK_URL"'",
      "content_type": "json",
      "secret": "'"$WEBHOOK_SECRET"'",
      "insecure_ssl": "0"
    }
  }')

# Check if the webhook was created successfully
if echo "$response" | grep -q "\"id\""; then
    echo "Webhook created successfully!"
    echo "Response:"
    echo "$response" | grep "\"id\""
else
    echo "Failed to create webhook:"
    echo "$response"
    exit 1
fi

echo "Webhook setup complete!"
