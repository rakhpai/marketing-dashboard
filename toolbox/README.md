# MCP Toolbox for Marketing Dashboard

This directory contains the MCP Toolbox for Databases setup for the Marketing Dashboard project.

## What is MCP Toolbox?

MCP Toolbox for Databases (formerly GenAI Toolbox) is an MCP-compatible server that allows AI assistants to interact with databases through predefined tools.

## Setup

The toolbox has already been installed in this directory with a sample configuration in `tools.yaml`.

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

Update the database connection details in `tools.yaml` to match your actual database:

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

### Testing

Use the provided Python script to test the toolbox:

```bash
# First install the SDK (if not already installed)
pip install toolbox-core

# Then run the test script
python test_toolbox.py
```

## Using with AI Assistants

### With Claude

When using Claude, provide the MCP URL:

```
mcp://localhost:5000/toolsets/marketing_analytics
```

### With Claude Code CLI

```bash
claude-code --mcp-server http://localhost:5000/toolsets/marketing_analytics
```

## Troubleshooting

- Check logs: `sudo journalctl -u mcp-toolbox`
- Verify connection: `curl http://localhost:5000/v1/health`
- Test tools directly: `curl http://localhost:5000/v1/tools`

## Documentation

For more detailed documentation, see the [official MCP Toolbox documentation](https://github.com/googleapis/genai-toolbox).