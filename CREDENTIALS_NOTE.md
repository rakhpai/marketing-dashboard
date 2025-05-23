# Important: Google Cloud Credentials Location

## Available Credentials Files

The Google Cloud service account credentials for BigQuery access are available at these locations:

1. **Primary location** (currently configured but has restrictive permissions):
   - Path: `/var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json`
   - Permissions: `-rw-r----- 1 root psaserv` (not readable by the application user)

2. **Alternative location** (accessible):
   - Path: `/var/www/vhosts/fgtwelve.ltd/seo_application/seo-twelve/seo-integration-key.json`
   - Permissions: `-rw-r----- 1 root psaserv` (also restrictive)

## Current Issue

The marketing dashboard is configured to use the primary location, but the file permissions prevent the application user (`fgtwelve.ltd_7n3kakd1pn9`) from reading it.

## Solutions

### Option 1: Fix Permissions (Recommended)
```bash
sudo chmod 644 /var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json
```

### Option 2: Copy to User Directory
```bash
sudo cp /var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/
sudo chown fgtwelve.ltd_7n3kakd1pn9:psacln /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/seo-integration-key.json
```

### Option 3: Update Configuration
Update `src/config/settings.py` to use the alternative path:
```python
google_credentials_path: str = "/var/www/vhosts/fgtwelve.ltd/seo_application/seo-twelve/seo-integration-key.json"
```

## BigQuery Configuration

- **Project ID**: `gtm-management-twelvetransfers`
- **Dataset**: `seo_data`
- **Tables Available**:
  - `search_console_data` - Google Search Console metrics
  - `keyword_positions` - Competitor keyword tracking

## Security Note

The service account key file contains sensitive credentials. Ensure:
1. File permissions are restrictive (readable only by necessary users)
2. Never commit this file to version control
3. Consider using environment variables or secret management services in production

## Testing Connection

To test if the credentials are working:
1. Click "Test Data Connection" in the dashboard sidebar
2. Or run: `sudo -u fgtwelve.ltd_7n3kakd1pn9 python3 -c "from src.data import test_bigquery_connection; print(test_bigquery_connection())"`

---
Last updated: 2025-05-23