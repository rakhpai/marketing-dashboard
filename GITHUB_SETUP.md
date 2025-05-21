# GitHub Repository Setup Instructions

To push this local repository to GitHub, follow these steps:

1. Create a new GitHub repository at https://github.com/new
   - Repository name: marketing-dashboard
   - Description: Streamlit-based marketing dashboard for Twelve Transfers
   - Choose either public or private visibility as needed

2. After creating the repository, run the following commands:

```bash
# Navigate to the repository
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/marketing-dashboard.git

# Push the repository to GitHub
git push -u origin master
```

3. If you're using GitHub authentication, you'll need to provide your credentials.

## Using GitHub CLI (Alternative Approach)

If you have GitHub CLI installed, you can create and push to a repository in one step:

```bash
# Navigate to the repository
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing

# Create a new repository and push
gh repo create marketing-dashboard --private --source=. --push
```

## Setting Up GitHub Actions (Optional)

Once the repository is on GitHub, you might want to set up GitHub Actions for CI/CD:

1. Create a `.github/workflows` directory
2. Add a workflow file (e.g., `deploy.yml`) to automate testing and deployment

This will allow for automated updates to the dashboard whenever changes are pushed to the repository.