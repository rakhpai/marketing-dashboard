# GitHub Personal Access Token Instructions

To log in to GitHub CLI and create/push to your repository, you'll need to create a Personal Access Token.

## Step 1: Generate a Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click on "Generate new token" > "Generate new token (classic)"
3. Give your token a descriptive name, e.g., "Marketing Dashboard Push"
4. Set the expiration as appropriate (e.g., 30 days)
5. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (if you plan to use GitHub Actions)
   - `admin:org` > `read:org` (only if you need org access)
6. Click "Generate token"
7. **IMPORTANT**: Copy the token immediately, as you won't be able to see it again!

## Step 2: Login Using the Token

Once you have your token, run this command:

```bash
gh auth login --with-token
```

When prompted, paste your personal access token.

## Alternative: Store Token in File and Use It

You can also store the token in a temporary file and use it:

```bash
echo "YOUR_TOKEN_HERE" > /tmp/github-token.txt
gh auth login --with-token < /tmp/github-token.txt
rm /tmp/github-token.txt  # Remove the token file for security
```

## Step 3: Create and Push to Repository

After successful authentication, you can create and push to your repository:

```bash
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing
gh repo create marketing-dashboard --private --source=. --push
```

This will:
1. Create a new private repository called "marketing-dashboard"
2. Use the current directory as the source
3. Push your code to the new repository

## Security Note

- Never share your personal access token with anyone
- Don't store the token in any files that get committed to your repository
- Delete the token from GitHub when you no longer need it