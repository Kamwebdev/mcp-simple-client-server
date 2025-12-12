import pytest


@pytest.fixture
def mcp():
    class DummyMCP:
        def __init__(self):
            self.tools = {}

        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func

            return decorator

    return DummyMCP()
