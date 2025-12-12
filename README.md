# Mcp-simple-client-server

## Overview

mcp-simple-client-server is a minimal working example of the
Model Context Protocol (MCP) — showing how to:

- register tools on an MCP server,
- expose them to an LLM (Ollama, OpenAI-compatible),
- let the model call these tools dynamically,
- return results back into the conversation loop.

The project is intentionally simple and clean, making it an ideal starting point for building your own MCP-powered automations, assistants and local AI integrations.

## Install:
```
python -m venv .venv
.venv\Scripts\activate.bat
pip3 install -r requirements.txt
```

## Run:

### MCP Server

To start the mcp server, execute:
```
cd server
python mcp_server.py
```

#### How It Works
1. The server starts a FastMCP instance and registers all available tools.
2. FastMCP automatically exposes the tools over HTTP at /mcp.
3. The client (or LLM) can now remotely execute these tools through function calling.

#### Sample output:
[Server output](./server/outputs/server.md)

### Client

To run our mcp server client, execute in the second terminal
```
cd client
cp .env_dist .env
python client.py
```
#### Sample outputs:
- [llama3.1:8b](./client/outputs/client-llama3.1_8b.md)
- [gpt-oss:20b](./client/outputs/client-gpt-oss.md)

#### How It Works
1. The client connects to the MCP server.
2. It fetches registered tools.
3. Tools are forwarded to the LLM (via Ollama function calling).
4. The LLM may: answer normally or request tool execution.
5. The tool runs on the MCP server.
6. The result is returned to the LLM.
7. Loop continues until the model stops calling tools.
