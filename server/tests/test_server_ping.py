from unittest.mock import MagicMock, patch
from ..mcp_server import register_tools


def test_ping_online(mcp):
    register_tools(mcp)

    mock_response = MagicMock()
    mock_response.success.return_value = True
    mock_response.rtt_avg_ms = 10.0

    with patch("server.mcp_server.py_ping", return_value=mock_response):
        result = mcp.tools["ping"]("8.8.8.8")

    assert result == "8.8.8.8 - online"


def test_ping_offline(mcp):
    register_tools(mcp)

    mock_response = MagicMock()
    mock_response.success.return_value = False

    with patch("server.mcp_server.py_ping", return_value=mock_response):
        result = mcp.tools["ping"]("1.2.3.4")

    assert result == "1.2.3.4 - offline"


def test_ping_exception(mcp):
    register_tools(mcp)

    with patch("server.mcp_server.py_ping", side_effect=Exception("ping error")):
        result = mcp.tools["ping"]("example.com")

    assert result == "example.com - offline"
