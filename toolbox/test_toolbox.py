import asyncio
import json

# To use this script, you'll need to install the toolbox-core SDK:
# pip install toolbox-core
from toolbox_core import ToolboxClient

async def test_toolbox():
    # Connect to the toolbox server
    client = ToolboxClient("http://127.0.0.1:5000")
    
    # Load all tools from the marketing_analytics toolset
    tools = await client.load_toolset("marketing_analytics")
    
    print(f"Loaded {len(tools)} tools from the marketing_analytics toolset:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    # Example: Execute a tool
    try:
        # This is just a test - update with real parameters for your database schema
        result = await tools[0].execute({
            "start_date": "2023-01-01",
            "end_date": "2023-01-31",
            "channel": "Social Media"
        })
        print("\nTool execution result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\nError executing tool: {e}")

if __name__ == "__main__":
    asyncio.run(test_toolbox())