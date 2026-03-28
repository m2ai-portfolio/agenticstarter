"""
Tests for MCP Server (Feature 3)
"""

import json
import time
import pytest
from http.client import HTTPConnection
from agenticstarter.mcp_server import MCPServer


# Use incrementing port numbers to avoid conflicts
_test_port_counter = 8100


def get_test_port():
    """Get a unique port number for each test."""
    global _test_port_counter
    port = _test_port_counter
    _test_port_counter += 1
    return port


@pytest.fixture
def server():
    """Fixture to create and manage an MCP server for testing."""
    port = get_test_port()
    server_instance = MCPServer(host="localhost", port=port)
    server_instance.start(blocking=False)

    # Give server time to start
    time.sleep(0.2)

    yield server_instance

    # Clean up
    server_instance.stop()
    time.sleep(0.1)


def send_jsonrpc_request(host, port, method, params=None, request_id=1):
    """
    Helper function to send a JSON-RPC 2.0 request to the server.

    Args:
        host: Server host
        port: Server port
        method: JSON-RPC method name
        params: Method parameters (optional)
        request_id: Request ID

    Returns:
        Parsed JSON response
    """
    conn = HTTPConnection(host, port)

    request_body = {
        "jsonrpc": "2.0",
        "method": method,
        "id": request_id
    }

    if params is not None:
        request_body["params"] = params

    headers = {"Content-Type": "application/json"}
    conn.request("POST", "/", json.dumps(request_body), headers)

    response = conn.getresponse()
    response_data = response.read()
    conn.close()

    return json.loads(response_data.decode('utf-8'))


def test_server_starts_and_accepts_connections(server):
    """Test that the MCP server starts and accepts HTTP connections."""
    conn = HTTPConnection("localhost", server.port)
    try:
        conn.connect()
        assert True  # Connection successful
    finally:
        conn.close()


def test_ping_pong_basic(server):
    """Test basic ping/pong functionality."""
    response = send_jsonrpc_request("localhost", server.port, "ping")

    assert response["jsonrpc"] == "2.0"
    assert response["result"] == "pong"
    assert response["id"] == 1


def test_ping_pong_with_different_id(server):
    """Test that response ID matches request ID."""
    response = send_jsonrpc_request("localhost", server.port, "ping", request_id=42)

    assert response["jsonrpc"] == "2.0"
    assert response["result"] == "pong"
    assert response["id"] == 42


def test_unknown_method_returns_error(server):
    """Test that calling an unknown method returns a JSON-RPC error."""
    response = send_jsonrpc_request("localhost", server.port, "unknown_method")

    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32601
    assert "Method not found" in response["error"]["message"]
    assert response["id"] == 1


def test_jsonrpc_format_compliance(server):
    """Test that responses comply with JSON-RPC 2.0 format."""
    response = send_jsonrpc_request("localhost", server.port, "ping")

    # Must have jsonrpc field with value "2.0"
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"

    # Must have either result or error, not both
    assert ("result" in response) != ("error" in response)

    # Must have id field
    assert "id" in response


def test_invalid_json_returns_parse_error(server):
    """Test that invalid JSON returns a parse error."""
    conn = HTTPConnection("localhost", server.port)
    headers = {"Content-Type": "application/json"}
    conn.request("POST", "/", "not valid json", headers)

    response = conn.getresponse()
    response_data = response.read()
    conn.close()

    parsed_response = json.loads(response_data.decode('utf-8'))

    assert parsed_response["jsonrpc"] == "2.0"
    assert "error" in parsed_response
    assert parsed_response["error"]["code"] == -32700
    assert "Parse error" in parsed_response["error"]["message"]


def test_tool_registration_and_invocation(server):
    """Test that custom tools can be registered and invoked."""

    # Register a custom tool
    def custom_tool(params):
        return {"status": "success", "input": params}

    server.register_tool("custom_tool", custom_tool)

    # Invoke the custom tool
    response = send_jsonrpc_request(
        "localhost", server.port, "custom_tool", params={"test": "data"}
    )

    assert response["jsonrpc"] == "2.0"
    assert response["result"]["status"] == "success"
    assert response["result"]["input"]["test"] == "data"


def test_tool_with_complex_params(server):
    """Test tool invocation with complex parameter structures."""

    def summarize_tool(params):
        text = params.get("text", "")
        max_length = params.get("max_length", 100)
        return {
            "summary": text[:max_length],
            "length": len(text),
            "truncated": len(text) > max_length
        }

    server.register_tool("summarize", summarize_tool)

    response = send_jsonrpc_request(
        "localhost", server.port,
        "summarize",
        params={"text": "This is a long text" * 10, "max_length": 20}
    )

    assert response["jsonrpc"] == "2.0"
    assert "result" in response
    assert response["result"]["truncated"] is True
    assert len(response["result"]["summary"]) == 20


def test_multiple_tool_registrations(server):
    """Test that multiple tools can be registered independently."""

    def tool_a(params):
        return "result_a"

    def tool_b(params):
        return "result_b"

    server.register_tool("tool_a", tool_a)
    server.register_tool("tool_b", tool_b)

    response_a = send_jsonrpc_request("localhost", server.port, "tool_a")
    response_b = send_jsonrpc_request("localhost", server.port, "tool_b")

    assert response_a["result"] == "result_a"
    assert response_b["result"] == "result_b"


def test_tool_exception_handling(server):
    """Test that exceptions in tool handlers are caught and returned as errors."""

    def failing_tool(params):
        raise RuntimeError("Tool failed intentionally")

    server.register_tool("failing_tool", failing_tool)

    response = send_jsonrpc_request("localhost", server.port, "failing_tool")

    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32603
    assert "Internal error" in response["error"]["message"]


def test_server_stop(server):
    """Test that server can be stopped gracefully."""
    port = server.port

    # Server is running (from fixture)
    response = send_jsonrpc_request("localhost", port, "ping")
    assert response["result"] == "pong"

    # Stop the server
    server.stop()

    # Give it time to shutdown
    time.sleep(0.2)

    # Attempt to connect should fail
    with pytest.raises(Exception):
        send_jsonrpc_request("localhost", port, "ping")
