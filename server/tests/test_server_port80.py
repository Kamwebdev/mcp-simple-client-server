from unittest.mock import MagicMock, patch
from ..mcp_server import register_tools


def test_check_port_open(mcp):
    register_tools(mcp)

    with patch("server.mcp_server.socket.socket") as mock_socket_cls:
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0

        mock_socket_cls.return_value.__enter__.return_value = mock_socket

        result = mcp.tools["check_port_80"]("example.com")

    assert result == "example.com - port 80 open"


def test_check_port_closed(mcp):
    register_tools(mcp)

    with patch("server.mcp_server.socket.socket") as mock_socket_cls:
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 111

        mock_socket_cls.return_value.__enter__.return_value = mock_socket

        result = mcp.tools["check_port_80"]("example.com")

    assert result == "example.com - port 80 closed"


def test_check_port_exception(mcp):
    register_tools(mcp)

    with patch("server.mcp_server.socket.socket") as mock_socket_cls:
        mock_socket = MagicMock()
        mock_socket.connect_ex.side_effect = Exception("socket failure")

        mock_socket_cls.return_value.__enter__.return_value = mock_socket

        result = mcp.tools["check_port_80"]("example.com")

    assert result == "example.com - port 80 closed"
