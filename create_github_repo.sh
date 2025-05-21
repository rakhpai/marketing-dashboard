#!/bin/bash

# Create GitHub repository and push marketing dashboard code
# This script must be run after you are logged in to GitHub CLI

echo "===== Creating GitHub Repository and Pushing Code ====="

# Check if GitHub CLI is authenticated
if ! gh auth status 2>/dev/null; then
  echo "Error: Not logged in to GitHub CLI."
  echo "Please run 'gh auth login' first and complete the authentication."
  exit 1
fi

# Go to the marketing dashboard directory
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing || {
  echo "Error: Could not change to marketing directory."
  exit 1
}

# Create the repository
echo "Creating GitHub repository 'marketing-dashboard'..."
gh repo create marketing-dashboard --private --description "Streamlit-based marketing dashboard for Twelve Transfers" || {
  echo "Error: Could not create repository. It might already exist."
  
  # Check if repository exists
  if gh repo view rakhpai/marketing-dashboard >/dev/null 2>&1; then
    echo "Repository 'rakhpai/marketing-dashboard' already exists."
  else
    exit 1
  fi
}

# Push the code
echo "Pushing code to GitHub..."
git push -u origin master

# Verify the push was successful
if [ $? -eq 0 ]; then
  echo "===== Success! ====="
  echo "Repository URL: https://github.com/rakhpai/marketing-dashboard"
  echo "GitMCP URL: https://gitmcp.io/rakhpai/marketing-dashboard"
  echo ""
  echo "You can now use the GitMCP URL with AI tools for enhanced code context."
else
  echo "Error: Failed to push code to GitHub."
  exit 1
fi