# Marketing Dashboard Status Report

## Overview

This document provides information about the current status of the Marketing Dashboard.

## Configuration Details

- **Dashboard URL**: https://fgtwelve.ltd/marketing/
- **Internal URL**: http://localhost:9005/marketing/
- **Service**: `streamlit-marketing.service` (systemd)
- **Application Port**: 9005
- **Nginx Configuration**: `/var/www/vhosts/system/fgtwelve.ltd/conf/vhost_nginx.conf`

## Service Status

The Streamlit Marketing Dashboard service is currently:
- **ACTIVE** - Running as expected
- Using port 9005
- Configured with proper WebSocket support

## Nginx Configuration

The current Nginx configuration for the Marketing Dashboard:

```nginx
# Marketing Dashboard (Streamlit)
location /marketing/ {
    proxy_pass http://127.0.0.1:9005/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
    proxy_buffering off;
    proxy_read_timeout 300s;
}

# Static files for Marketing Dashboard
location /marketing/_stcore/ {
    proxy_pass http://127.0.0.1:9005/_stcore/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
}

# Stream support for Marketing Dashboard
location /marketing/stream {
    proxy_pass http://127.0.0.1:9005/stream;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_buffering off;
}
```

## Management Commands

```bash
# Check service status
sudo systemctl status streamlit-marketing.service

# Restart service
sudo systemctl restart streamlit-marketing.service

# View logs
sudo journalctl -u streamlit-marketing.service -n 50

# Test direct access
curl -s -I http://localhost:9005/marketing/
```

## Notes

- The Marketing Dashboard is separate from the other dashboards (SEO and SEO-Data)
- WebSocket connections are properly configured for real-time updates
- The dashboard application is installed at `/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/`
- Sample data is currently used - this can be replaced with real data sources

## Last Updated

`$(date '+%Y-%m-%d %H:%M:%S')`