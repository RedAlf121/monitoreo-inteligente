import os
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import create_session
from dill import dump, loads
import time

def load_mcp_config_from_json():
    mcp_file_path = os.path.join('mcp.json')
    with open(mcp_file_path, 'r') as file:
        mcp_config = json.load(file)
    return mcp_config["mcpServers"]

async def load_tools_from_mcp(mcp_config: dict = load_mcp_config_from_json()):
        
    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()
    return tools

async def get_tools_with_cache(mcp_config:dict, retries: int = 5, cache_file: str = "tools.pkl"):
    if not os.path.exists(cache_file):
        open(cache_file, 'x').close()
    while True:
        try:
            if retries > 0:
                tools = await load_tools_from_mcp()
                print("Tools loaded from MCP.")
                with open(cache_file, "wb") as f:
                    dump(tools, f)
            else:
                print("Failed to load tools after multiple attempts. Loading from cache...")
                with open(cache_file, "rb") as f:
                    tools = loads(f.read())
            break
        except EOFError:
            raise EOFError("Cache empty. Try again")
        except Exception as e:
            print(f"Error loading tools: {e}")
            e.with_traceback()
            time.sleep(2)
            retries -= 1
    return tools
