import asyncio
import json
from fastmcp import Client
import ollama

from utils.printer import nice_print
from dotenv import load_dotenv
import os

load_dotenv()

MCP_URL = os.getenv("MCP_URL")
USER_PROMPT = os.getenv("USER_PROMPT")
MODEL = os.getenv("MODEL")


async def mcp_client():
    """
    Connects to the MCP server, retrieves available tools, and runs a loop where
    a local LLM (Ollama) can call these tools until a final answer is produced.
    """
    client = Client(MCP_URL)

    async with client:
        tools = await client.list_tools()

        ollama_tools = []
        for t in tools:
            ollama_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": t.inputSchema,
                    },
                }
            )

        nice_print("Tool list from MCP server", ollama_tools)
        messages = [{"role": "user", "content": USER_PROMPT}]

        while True:
            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools,
            )

            msg = response["message"]
            nice_print("Recived answer from LLM", msg)

            if "tool_calls" not in msg:
                break

            tool_calls = msg["tool_calls"]
            nice_print("Tools called", tool_calls)

            messages.append(
                {"role": "assistant", "content": "", "tool_calls": tool_calls}
            )

            for call in tool_calls:
                name = call["function"]["name"]
                args = call["function"].get("arguments", {})

                tool_result = await client.call_tool(name, args)
                messages.append(
                    {
                        "role": "tool",
                        "name": name,
                        "content": json.dumps({"result": tool_result.data}),
                    }
                )

        nice_print("Full chat history", messages)
        nice_print("Final answer", response["message"]["content"])


if __name__ == "__main__":
    asyncio.run(mcp_client())
