# Complete GitHub Setup Guide

This guide provides step-by-step instructions to get your marketing dashboard repository on GitHub and configure it for GitMCP.

## Option 1: Using Personal Access Token (Recommended)

### Step 1: Generate a Personal Access Token on GitHub

1. Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" > "Generate new token (classic)"
3. Give it a descriptive name like "Marketing Dashboard Setup"
4. Set expiration as needed (e.g., 7 days)
5. Select these scopes:
   - `repo` (Full control of repositories)
   - `workflow` (if you plan to use GitHub Actions)
6. Click "Generate token"
7. **IMPORTANT**: Copy the generated token immediately

### Step 2: Use the Token to Login

```bash
# On your server
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing

# Create a temporary file with your token (replace YOUR_TOKEN with the actual token)
echo "YOUR_TOKEN" > /tmp/github-token.txt

# Login using the token
gh auth login --with-token < /tmp/github-token.txt

# Remove the token file for security
rm /tmp/github-token.txt
```

### Step 3: Run the Repository Creation Script

```bash
./create_github_repo.sh
```

## Option 2: Using SSH Key

### Step 1: Check Existing SSH Key

The server already has an SSH key at `/root/.ssh/id_ed25519`. Ensure this key is added to your GitHub account.

1. View the public key:
   ```bash
   cat /root/.ssh/id_ed25519.pub
   ```

2. Add this key to your GitHub account at [GitHub Settings > SSH and GPG keys](https://github.com/settings/ssh/new)

### Step 2: Create Repository on GitHub Manually

1. Go to [GitHub New Repository](https://github.com/new)
2. Enter repository details:
   - Repository name: `marketing-dashboard`
   - Description: `Streamlit-based marketing dashboard for Twelve Transfers`
   - Visibility: Either private or public as preferred
   - Do NOT initialize with README, .gitignore, or license files
3. Click "Create repository"

### Step 3: Push Your Code to GitHub

```bash
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing

# Set the remote URL to SSH
git remote set-url origin git@github.com:rakhpai/marketing-dashboard.git

# Push the code
git push -u origin master
```

## Verify and Use with GitMCP

Regardless of which method you used, after pushing:

1. Verify your repository is available at:
   ```
   https://github.com/rakhpai/marketing-dashboard
   ```

2. Your GitMCP URL will be:
   ```
   https://gitmcp.io/rakhpai/marketing-dashboard
   ```

3. Use this GitMCP URL with Claude or other AI tools to get enhanced context about your code.

## Additional Commands

```bash
# Check GitHub authentication status
gh auth status

# View your repositories
gh repo list

# Create an issue
gh issue create --title "Issue title" --body "Issue description"

# Clone your repository to another location
gh repo clone rakhpai/marketing-dashboard
```