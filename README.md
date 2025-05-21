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

### Key Configuration Files

- **Streamlit App**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/app.py`
- **Systemd Service**: `/etc/systemd/system/streamlit-marketing.service`
- **Nginx Configuration**: Set in Plesk's vhost_nginx.conf

### Service Management

```bash
# Check status
sudo systemctl status streamlit-marketing.service

# Restart service
sudo systemctl restart streamlit-marketing.service

# View logs
sudo journalctl -u streamlit-marketing.service
```

## Implementation Details

- Running on port 9005
- WebSocket support for real-time updates
- Static assets cached via Nginx
- Systemd service ensures automatic restart on failure

See `DASHBOARD_STATUS.md` for current configuration status and details.