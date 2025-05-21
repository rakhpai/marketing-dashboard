# Push to GitHub Instructions

Since we couldn't automatically create and push to the GitHub repository, here are manual instructions to complete the setup:

## 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Enter the following details:
   - Repository name: **marketing-dashboard**
   - Description: **Streamlit-based marketing dashboard for Twelve Transfers**
   - Visibility: Public (or Private if you prefer)
   - Do NOT initialize with README, .gitignore, or license (as we already have these files)
3. Click "Create repository"

## 2. Push Existing Repository

After creating the repository, run these commands on the server:

```bash
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing
git push -u origin master
```

If you encounter authentication issues, make sure your GitHub SSH key is properly set up and has access to your GitHub account.

## 3. Verify Repository

After pushing, verify that all files are present in your GitHub repository by visiting:
https://github.com/rakhpai/marketing-dashboard

## 4. Use with GitMCP

Once your repository is on GitHub, you can use it with GitMCP by using this URL:
https://gitmcp.io/rakhpai/marketing-dashboard

Configure your AI tool to use this URL as an MCP server, and it will have enhanced context about your marketing dashboard code.

## Troubleshooting

If you encounter SSH key issues, you may need to:

1. Verify your SSH key is added to your GitHub account: https://github.com/settings/keys
2. Test your SSH connection: `ssh -T git@github.com`
3. Make sure your Git configuration is correct:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```