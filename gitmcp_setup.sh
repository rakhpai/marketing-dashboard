#!/bin/bash
# GitMCP Setup Script for Marketing Dashboard
# This script configures the necessary files for GitMCP integration

set -e  # Exit on error

echo "=== GitMCP Setup for Marketing Dashboard ==="

# Create or update llms.txt if it doesn't exist
if [ ! -f "llms.txt" ]; then
  echo "Creating llms.txt..."
  cat > llms.txt << EOL
# Twelve Transfers Marketing Dashboard

## Project Overview
A Streamlit-based marketing dashboard for Twelve Transfers, displaying key marketing metrics and KPIs including traffic, conversions, and revenue by channel.

## Main Components

- \`app.py\` - Main Streamlit application with dashboard UI and visualizations
- \`.streamlit/config.toml\` - Streamlit configuration for production deployment
- \`requirements.txt\` - Python dependencies
- \`restart_streamlit.sh\` & \`run_streamlit.sh\` - Service management scripts

## Infrastructure

- Deployed on Plesk server at path \`/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/\`
- Running as systemd service \`streamlit-marketing.service\` on port 9005
- Nginx configured to proxy requests from \`/marketing/\` path to the Streamlit app
- WebSocket connections properly configured for real-time updates

## API and Integration Points

- Uses Pandas for data manipulation
- Altair for interactive visualizations
- Currently using sample data that can be replaced with actual data sources

## Key Features

- Interactive charts showing channel performance
- Traffic and conversion metrics
- Filter capabilities by date range and channel
- Responsive design for desktop and mobile viewing
EOL
else
  echo "llms.txt already exists, skipping..."
fi

# Create or update llms-full.txt
if [ ! -f "llms-full.txt" ]; then
  echo "Creating llms-full.txt..."
  cat > llms-full.txt << EOL
# Twelve Transfers Marketing Dashboard

## Project Overview
A comprehensive Streamlit-based marketing dashboard for Twelve Transfers, displaying key marketing metrics and KPIs. This dashboard visualizes traffic, conversions, and revenue data by marketing channel.

## Directory Structure

\`\`\`
/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/
├── .streamlit/                    # Streamlit configuration
│   └── config.toml                # Production configuration
├── static/                        # Static assets
│   ├── css/
│   │   └── main.23bdda6f.css      # Stylesheet
│   ├── js/
│   │   └── main.75ac1cb6.js       # JavaScript
│   └── media/                     # Fonts
├── app.py                         # Main Streamlit dashboard application
├── requirements.txt               # Python dependencies
├── run_streamlit.sh               # Script to run the Streamlit app
├── restart_streamlit.sh           # Script to restart the service
├── README.md                      # Project documentation
├── DASHBOARD_STATUS.md            # Current deployment status
├── GITHUB_SETUP.md                # GitHub repository setup instructions
└── llms.txt                       # Project overview for AI tools
\`\`\`

## Implementation Details

### Main Application (\`app.py\`)

The dashboard is implemented using Streamlit, a Python framework for creating data applications. Key components:

1. **Dashboard Structure**:
   - Page configuration with wide layout
   - Sidebar with date range and channel filters
   - Main content area with metrics and visualizations

2. **Data Handling**:
   - Sample data generation (to be replaced with real data)
   - Data aggregation by channel and date
   - Conversion calculations

3. **Visualizations**:
   - Top metrics cards showing totals with delta indicators
   - Bar charts for channel performance
   - Line charts for time-series data
   - Detailed data tables

### Infrastructure Configuration

1. **Systemd Service**: 
   - Running on port 9005
   - Automatic restart on failure
   - Configuration file: \`/etc/systemd/system/streamlit-marketing.service\`

2. **Nginx Configuration**:
   - Path-based routing at \`/marketing/\`
   - WebSocket support for real-time updates
   - Static file caching
   - Configuration in Plesk's \`vhost_nginx.conf\`

3. **URL Access**:
   - Public URL: https://fgtwelve.ltd/marketing/
   - Internal URL: http://localhost:9005/marketing/

## Dependencies

The dashboard depends on several Python libraries:
- streamlit==1.40.1 - Main application framework
- pandas>=2.0.0 - Data manipulation
- numpy>=1.24.0 - Numerical operations
- altair>=5.0.0 - Interactive visualizations
- plotly>=5.3.0 - Additional chart options
- matplotlib>=3.5.0 - Static visualizations

## Future Development Plans

1. **Data Integration**:
   - Connect to actual marketing data sources
   - Implement Google Analytics integration
   - Add social media metrics

2. **Enhanced Features**:
   - User authentication
   - Scheduled reports
   - Export capabilities
   - Custom date comparisons

3. **UI Improvements**:
   - Custom theming
   - Additional visualization types
   - Drill-down capabilities
EOL
else
  echo "llms-full.txt already exists, skipping..."
fi

# Update README.md with GitMCP information
echo "Updating README.md with GitMCP information..."
if grep -q "GitMCP Integration" README.md; then
  echo "GitMCP information already in README.md, skipping..."
else
  cat >> README.md << EOL

## GitMCP Integration

This repository is configured for use with GitMCP, enabling AI assistants to better understand the codebase.

### How to Use with AI Tools

Once this repository is on GitHub, you can use it with GitMCP by:

1. Replace "github.com" with "gitmcp.io" in the repository URL
2. Configure your AI tool to use this URL as an MCP server
3. Your AI assistant will now have enhanced context about this marketing dashboard

Example:
- GitHub URL: https://github.com/YOUR_USERNAME/marketing-dashboard
- GitMCP URL: https://gitmcp.io/YOUR_USERNAME/marketing-dashboard
EOL
fi

# Update .gitignore to include GitMCP-specific files if needed
if ! grep -q "# GitMCP" .gitignore; then
  echo "Updating .gitignore..."
  cat >> .gitignore << EOL

# GitMCP
.gitmcp-cache/
EOL
fi

echo "=== GitMCP Setup Complete ==="
echo "The repository is now configured for GitMCP integration!"
echo "To use with AI tools, push to GitHub and use the gitmcp.io URL as described in the README."