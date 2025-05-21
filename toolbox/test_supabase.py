import asyncio
import json
import sys

# To use this script, you'll need to install the toolbox-core SDK:
# pip install toolbox-core
try:
    from toolbox_core import ToolboxClient
except ImportError:
    print("Error: toolbox-core package not installed")
    print("Please install it with: pip install toolbox-core")
    sys.exit(1)

async def test_supabase_tools():
    # Connect to the toolbox server
    client = ToolboxClient("http://127.0.0.1:5000")
    
    # Load only the Supabase toolset
    try:
        tools = await client.load_toolset("supabase_tools")
        print(f"Successfully loaded {len(tools)} Supabase tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
    except Exception as e:
        print(f"Error loading Supabase tools: {e}")
        return
    
    # Test each Supabase tool with sample parameters
    test_params = {
        "supabase-get-campaigns": {
            "status": "active",
            "limit": 10
        },
        "supabase-get-campaign-details": {
            "campaign_id": "12345"  # Replace with an actual campaign ID
        },
        "supabase-campaign-performance": {
            "campaign_id": "12345",  # Replace with an actual campaign ID
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        },
        "supabase-audience-insights": {
            "campaign_id": None,  # Get insights for all campaigns
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }
    }
    
    # Execute each tool
    for tool in tools:
        try:
            print(f"\nTesting {tool.name}...")
            result = await tool.execute(test_params.get(tool.name, {}))
            print(f"SUCCESS: {tool.name} returned {len(result) if isinstance(result, list) else 1} result(s)")
            print(json.dumps(result[:3] if isinstance(result, list) and len(result) > 3 else result, indent=2))
        except Exception as e:
            print(f"ERROR: Failed to execute {tool.name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_supabase_tools())