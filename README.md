# Marketing Dashboard

A Streamlit-based marketing dashboard for Twelve Transfers displaying key marketing metrics and KPIs.

## Features

- Interactive charts and visualizations
- Channel performance tracking
- Traffic and conversion metrics
- Dashboard filters by date range and marketing channel
- Real-time updates via WebSockets

## Installation

The dashboard is installed on the Plesk server and is accessible at:
https://fgtwelve.ltd/marketing/

### Local Development Setup

```bash
# Clone the repository
git clone <repository_url>

# Navigate to project directory
cd marketing

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Infrastructure Setup

The dashboard runs as a systemd service on the server with Nginx configured to proxy requests to the Streamlit application.

### Automated Deployment

This repository is configured with an automated deployment system that pulls and updates the server whenever code is pushed to the master branch.

- **Webhook Server**: Running on port 9876
- **Webhook URL**: https://fgtwelve.ltd/webhook
- **Deployment Script**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/deploy.sh`
- **Webhook Logs**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/webhook.log`

### Key Configuration Files

- **Streamlit App**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/app.py`
- **Systemd Service**: `/etc/systemd/system/streamlit-marketing.service`
- **Nginx Configuration**: Set in Plesk's vhost_nginx.conf
- **Webhook Service**: `/etc/systemd/system/marketing-webhook.service`

### Service Management

```bash
# Check Streamlit status
sudo systemctl status streamlit-marketing.service

# Restart Streamlit service
sudo systemctl restart streamlit-marketing.service

# Check Webhook status
sudo systemctl status marketing-webhook.service

# View Streamlit logs
sudo journalctl -u streamlit-marketing.service

# View Webhook logs
tail -f /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/webhook.log
```

## Implementation Details

- Running on port 9005
- WebSocket support for real-time updates
- Static assets cached via Nginx
- Systemd service ensures automatic restart on failure

See `DASHBOARD_STATUS.md` for current configuration status and details.
## AI Assistant Integration

This repository is configured with multiple tools to enhance AI assistant capabilities:

### 1. GitMCP Integration

GitMCP enables AI assistants to better understand the codebase structure.

#### How to Use with AI Tools

Once this repository is on GitHub, you can use it with GitMCP by:

1. Replace "github.com" with "gitmcp.io" in the repository URL
2. Configure your AI tool to use this URL as an MCP server
3. Your AI assistant will now have enhanced context about this marketing dashboard

Example:
- GitHub URL: https://github.com/YOUR_USERNAME/marketing-dashboard
- GitMCP URL: https://gitmcp.io/YOUR_USERNAME/marketing-dashboard

### 2. MCP Toolbox for Databases

MCP Toolbox allows AI assistants to directly query databases for generating insights.

#### Configured Data Sources:

- **PostgreSQL**: Local database for application metrics
- **Supabase**: Remote PostgreSQL database for campaign data
- **BigQuery**: Analytics data warehouse for marketing analytics

#### Service Management:

```bash
# Check status
sudo systemctl status mcp-toolbox.service

# Restart service
sudo systemctl restart mcp-toolbox.service

# View logs
sudo journalctl -u mcp-toolbox.service
```

Configuration files:
- **Tools Config**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/toolbox/tools.yaml`
- **Status Report**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/toolbox/MCP_TOOLBOX_STATUS.md`
