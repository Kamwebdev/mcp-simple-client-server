from ..mcp_server import register_tools


def test_register_tools_registers_functions(mcp):
    register_tools(mcp)

    assert "ping" in mcp.tools
    assert "check_port_80" in mcp.tools
