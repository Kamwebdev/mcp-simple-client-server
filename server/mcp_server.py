import logging
import socket
from fastmcp import FastMCP
from pythonping import ping as py_ping

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s \t%(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


def register_tools(mcp: FastMCP) -> None:
    """
    Registers available tools within the given MCP server instance.

    Args:
        mcp (FastMCP): The FastMCP server instance to which the tools will be added.

    Returns:
        None
    """

    @mcp.tool()
    def ping(host: str) -> str:
        """
        Sends an ICMP echo (ping) request to the specified host and returns its network status.

        Args:
            host (str): The target hostname or IP address to check (e.g., "8.8.8.8" or "example.com").

        Returns:
            str: One of the following status values:
                - `"online"` – if the host responded successfully to the ping request
                - `"offline"` – if the host did not respond or a timeout/error occurred
                - `"invalid"` – if the input parameter is missing or invalid
        """
        logger.info(f'"PING {host}"')
        try:
            response = py_ping(host, count=1, timeout=2)
            if response.success():
                msg = f'"PING {host}" 200 OK (czas: {response.rtt_avg_ms:.1f} ms)'
                logger.debug(msg)
                return f"{host} - online"
            else:
                msg = f'"PING {host}" 408 TIMEOUT'
                logger.warning(msg)
                return f"{host} - offline"
        except Exception as e:
            msg = f'"PING {host}" 500 ERROR ({e})'
            logger.error(msg)
            return f"{host} - offline"

    @mcp.tool()
    def check_port_80(host: str) -> str:
        """
        Checks whether TCP port 80 on the given host is open.

        Args:
            host (str): The target hostname or IP.

        Returns:
            str: "<host> - port 80 open" or "<host> - port 80 closed"
        """
        logger.info(f'"PORT80 {host}"')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, 80))

                if result == 0:
                    msg = f'"PORT80 {host}" 200 OPEN'
                    logger.debug(msg)
                    return f"{host} - port 80 open"
                else:
                    msg = f'"PORT80 {host}" 403 CLOSED'
                    logger.warning(msg)
                    return f"{host} - port 80 closed"

        except Exception as e:
            msg = f'"PORT80 {host}" 500 ERROR ({e})'
            logger.error(msg)
            return f"{host} - port 80 closed"


def main() -> None:
    """
    Initializes the MCP server, registers tools, and starts the HTTP service.
    """
    server = FastMCP()
    register_tools(server)
    logger.info("Starting MCP Ping Server on http://127.0.0.1:8000/mcp")
    server.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")


if __name__ == "__main__":
    main()
