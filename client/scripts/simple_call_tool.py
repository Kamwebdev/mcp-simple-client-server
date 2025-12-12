import asyncio
from fastmcp import Client, FastMCP

server = FastMCP()
client = Client("http://127.0.0.1:8000/mcp")


async def main():
    async with client:
        await client.ping()

        # List available operations from server
        tools = await client.list_tools()
        # resources = await client.list_resources()
        # prompts = await client.list_prompts()

        result = await client.call_tool("ping", {"host": "127.0.0.1"})
        print(result)

asyncio.run(main())
