# MCP Toolbox for Marketing Dashboard

This directory contains the MCP Toolbox for Databases setup for the Marketing Dashboard project.

## What is MCP Toolbox?

MCP Toolbox for Databases (formerly GenAI Toolbox) is an MCP-compatible server that allows AI assistants to interact with databases through predefined tools.

## Supported Databases

The toolbox is configured to work with multiple database types:

- **PostgreSQL**: For operational marketing data
- **BigQuery**: For analytics and larger datasets
- **Supabase**: For real-time campaign management and audience insights

## Setup

The toolbox has already been installed in this directory with a configuration in `tools.yaml`.

## Usage

### Starting the Server

You can start the server using the provided script:

```bash
./run_toolbox.sh
```

Or use the systemd service:

```bash
sudo systemctl start mcp-toolbox
sudo systemctl enable mcp-toolbox  # To start on boot
```

### Configuration

The main configuration file is `tools.yaml`, which defines:

1. **Sources**: Database connections
2. **Tools**: SQL queries that AI assistants can use
3. **Toolsets**: Groups of tools that can be loaded together

#### PostgreSQL Configuration

Update the PostgreSQL connection details in `tools.yaml`:

```yaml
sources:
  marketing-db:
    kind: postgres
    host: YOUR_DB_HOST
    port: YOUR_DB_PORT
    database: YOUR_DB_NAME
    user: YOUR_DB_USER
    password: YOUR_DB_PASSWORD
```

#### BigQuery Configuration

The BigQuery connection uses a service account key file:

```yaml
sources:
  bigquery-analytics:
    kind: bigquery
    credentials_file: /var/www/vhosts/fgtwelve.ltd/env_files/seo_secrets/seo-integration-key.json
    project_id: twelve-marketing-analytics
    dataset_id: marketing_data
```

#### Supabase Configuration

Supabase is accessed via its PostgreSQL connection:

```yaml
sources:
  supabase-marketing:
    kind: postgres
    host: db.your-project.supabase.co
    port: 5432
    database: postgres
    user: postgres
    password: YOUR_SUPABASE_DB_PASSWORD
    ssl_mode: require
```

### Testing

Several test scripts are provided:

```bash
# First install the SDK (if not already installed)
pip install toolbox-core

# Test all tools
python test_toolbox.py

# Test only BigQuery tools
python test_bigquery.py

# Test only Supabase tools
python test_supabase.py
```

## Available Toolsets

The following toolsets are available:

1. **marketing_analytics**: All tools (PostgreSQL, BigQuery, and Supabase)
2. **postgres_tools**: Only PostgreSQL tools
3. **bigquery_tools**: Only BigQuery tools
4. **supabase_tools**: Only Supabase tools

## Using with AI Assistants

### With Claude

When using Claude, provide the MCP URL for the desired toolset:

```
mcp://localhost:5000/toolsets/marketing_analytics
```

Or for specific database tools:

```
mcp://localhost:5000/toolsets/bigquery_tools
mcp://localhost:5000/toolsets/supabase_tools
```

### With Claude Code CLI

```bash
claude-code --mcp-server http://localhost:5000/toolsets/marketing_analytics
```

## BigQuery Tools

The following BigQuery tools are available:

### 1. bq-campaign-performance

Get detailed campaign performance metrics.

Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `campaign_id`: Optional campaign ID filter

### 2. bq-channel-roi

Calculate ROI metrics by marketing channel.

Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

### 3. bq-keyword-performance

Analyze search keyword performance.

Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `min_impressions`: Minimum impressions threshold

## Supabase Tools

The following Supabase tools are available:

### 1. supabase-get-campaigns

Retrieve a list of marketing campaigns.

Parameters:
- `status`: Filter by campaign status (active, paused, completed)
- `limit`: Maximum number of campaigns to return

### 2. supabase-get-campaign-details

Get detailed information about a specific campaign, including channels and tags.

Parameters:
- `campaign_id`: ID of the campaign

### 3. supabase-campaign-performance

Get performance metrics for a specific campaign.

Parameters:
- `campaign_id`: ID of the campaign
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

### 4. supabase-audience-insights

Get audience demographics and interests data.

Parameters:
- `campaign_id`: Optional campaign ID filter
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

## Troubleshooting

- Check logs: `sudo journalctl -u mcp-toolbox`
- Verify connection: `curl http://localhost:5000/v1/health`
- Test tools directly: `curl http://localhost:5000/v1/tools`

## Documentation

For more detailed documentation, see the [official MCP Toolbox documentation](https://github.com/googleapis/genai-toolbox).