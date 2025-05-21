#!/bin/bash

# Run MCP Toolbox for Databases
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/toolbox

# Set environment variables if needed
# export DB_PASSWORD="your_secure_password"

# Start the server
./toolbox --tools-file "tools.yaml" --port 5000 --verbose