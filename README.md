

## Install
```
python -m venv .venv
.venv\Scripts\activate.bat
pip3 install -r requirements.txt
```

## Run

### MCP Server

To start the mcp server, execute:
```
cd server
python mcp_server.py
```
[Sample output](./server/outputs/server.md)

### Client

To run our mcp server client, execute in the second terminal
```
cd client
cp .env_dist .env
python client.py
```
Sample outputs:
- [llama3.1:8b](./client/outputs/client-llama3.1_8b.md)
- [gpt-oss:20b](./client/outputs/client-gpt-oss.md)