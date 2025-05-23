# Automated Deployment for Marketing Dashboard

This directory contains scripts and configuration files for automating the deployment of the Marketing Dashboard application.

## Deployment Options

There are two main deployment options:

1. **GitHub Webhook Server**: A simple webhook server that listens for GitHub push events and triggers deployment.
2. **GitHub Actions with Ansible**: Uses GitHub Actions to trigger an Ansible playbook for deployment.

## Option 1: GitHub Webhook Server

### Setup Instructions

1. **Copy the deployment files to your server**:
   ```bash
   scp -r deploy/ user@your-server:/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/
   ```

2. **Make the scripts executable**:
   ```bash
   ssh user@your-server "chmod +x /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/*.sh"
   ```

3. **Run the setup script**:
   ```bash
   ssh user@your-server "sudo /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/setup_webhook.sh your_webhook_secret"
   ```

4. **Configure GitHub webhook**:
   - Go to your GitHub repository settings
   - Click on "Webhooks" > "Add webhook"
   - Set Payload URL to `https://api.fgtwelve.ltd:9876/`
   - Set Content type to `application/json`
   - Set Secret to the same secret you used in the setup script
   - Select "Just the push event"
   - Click "Add webhook"

### How It Works

1. When you push to the master branch, GitHub sends a webhook event to your server.
2. The webhook server validates the request and triggers the deployment script.
3. The deployment script pulls the latest changes and restarts the application if necessary.

## Option 2: GitHub Actions with Ansible

### Setup Instructions

1. **Configure GitHub repository secrets**:
   - Go to your GitHub repository settings
   - Click on "Secrets" > "New repository secret"
   - Add the following secrets:
     - `SSH_PRIVATE_KEY`: Your SSH private key for accessing the server
     - `SERVER_IP`: Your server's IP address

2. **Update the Ansible inventory file**:
   - Edit `deploy/ansible/inventory.ini` with your server details

3. **Push the changes to GitHub**:
   ```bash
   git add .github/workflows/deploy.yml deploy/ansible/
   git commit -m "Add GitHub Actions deployment workflow"
   git push origin master
   ```

### How It Works

1. When you push to the master branch, GitHub Actions workflow is triggered.
2. The workflow runs the Ansible playbook to deploy the application.
3. Ansible connects to your server via SSH, pulls the latest changes, and restarts the application if necessary.

## Manual Deployment

If you need to deploy manually, you can run the deployment script directly:

```bash
ssh user@your-server "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/deploy.sh"
```

Or run the Ansible playbook locally:

```bash
cd deploy/ansible
ansible-playbook -i inventory.ini deploy.yml
```
