# Marketing Dashboard

This is a Streamlit-based marketing dashboard for fgtwelve.ltd.

## Setup Information

The dashboard is powered by Streamlit and is configured as follows:

- **App Location**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/app.py`
- **URL**: https://fgtwelve.ltd/marketing/
- **Service**: systemd service named `streamlit-marketing.service`

## Architecture

1. **Streamlit Application**: Python-based web application running on port 8501
2. **Nginx Configuration**: Proxies requests from /marketing to the Streamlit app
3. **WebSocket Support**: Configured for real-time updates in the dashboard

## Management Commands

### Service Management

```bash
# Start the service
sudo systemctl start streamlit-marketing.service

# Stop the service
sudo systemctl stop streamlit-marketing.service

# Restart the service
sudo systemctl restart streamlit-marketing.service

# Check service status
sudo systemctl status streamlit-marketing.service
```

### Quick Restart

```bash
# Using the provided script
sudo /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/restart_streamlit.sh
```

### Logs

```bash
# View Streamlit logs
sudo journalctl -u streamlit-marketing.service

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Maintenance

To update the dashboard:

1. Edit the main app file at `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/app.py`
2. Restart the Streamlit service: `sudo systemctl restart streamlit-marketing.service`

## Configuration Files

- **Streamlit Config**: `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/.streamlit/config.toml`
- **Nginx Config**: `/var/www/vhosts/fgtwelve.ltd/conf/vhost.conf`
- **Systemd Service**: `/etc/systemd/system/streamlit-marketing.service`