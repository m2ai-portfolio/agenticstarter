"""Tests for the MCP Server module."""

import json
import socket
import threading
import time
from urllib.request import urlopen, Request
from urllib.error import URLError
from agenticstarter.mcp_server import MCPServer


def test_handle_ping_request():
    """Test that server handles ping requests correctly."""
    server = MCPServer(port=8765)
    request = {
        'jsonrpc': '2.0',
        'method': 'ping',
        'id': 1
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert response['result'] == 'pong'
    assert response['id'] == 1


def test_handle_invalid_method():
    """Test that server handles invalid method requests."""
    server = MCPServer(port=8765)
    request = {
        'jsonrpc': '2.0',
        'method': 'invalid_method',
        'id': 2
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert 'error' in response
    assert response['error']['code'] == -32601
    assert 'Method not found' in response['error']['message']
    assert response['id'] == 2


def test_handle_missing_jsonrpc_version():
    """Test that server validates JSON-RPC version."""
    server = MCPServer(port=8765)
    request = {
        'method': 'ping',
        'id': 3
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert 'error' in response
    assert response['error']['code'] == -32600
    assert 'jsonrpc version must be 2.0' in response['error']['message']


def test_handle_missing_method():
    """Test that server validates method field."""
    server = MCPServer(port=8765)
    request = {
        'jsonrpc': '2.0',
        'id': 4
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert 'error' in response
    assert response['error']['code'] == -32600
    assert 'method is required' in response['error']['message']


def test_handle_invalid_request_type():
    """Test that server handles non-dict requests."""
    server = MCPServer(port=8765)
    request = "not a dict"
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert 'error' in response
    assert response['error']['code'] == -32600
    assert response['error']['message'] == 'Invalid Request'


def test_register_custom_method():
    """Test agentic execution embed - register custom method."""
    server = MCPServer(port=8765)

    def custom_handler(request):
        params = request.get('params', {})
        return {'status': 'success', 'data': params}

    server.register_method('custom_action', custom_handler)

    request = {
        'jsonrpc': '2.0',
        'method': 'custom_action',
        'params': {'key': 'value'},
        'id': 5
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert response['result']['status'] == 'success'
    assert response['result']['data']['key'] == 'value'
    assert response['id'] == 5


def test_custom_method_error_handling():
    """Test that custom method errors are handled properly."""
    server = MCPServer(port=8765)

    def failing_handler(request):
        raise ValueError("Custom error")

    server.register_method('failing_method', failing_handler)

    request = {
        'jsonrpc': '2.0',
        'method': 'failing_method',
        'id': 6
    }
    response = server.handle_request(request)

    assert response['jsonrpc'] == '2.0'
    assert 'error' in response
    assert response['error']['code'] == -32603
    assert 'Custom error' in response['error']['message']


def find_free_port():
    """Find a free port for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def test_server_http_ping_request():
    """Test that server responds to HTTP POST ping requests."""
    port = find_free_port()
    server = MCPServer(host='localhost', port=port)

    # Start server in background thread
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(0.5)

    try:
        # Send ping request
        request_data = json.dumps({'jsonrpc': '2.0', 'method': 'ping', 'id': 1}).encode('utf-8')
        request = Request(
            f'http://localhost:{port}',
            data=request_data,
            headers={'Content-Type': 'application/json'}
        )
        response = urlopen(request, timeout=2)

        assert response.status == 200
        data = json.loads(response.read().decode('utf-8'))
        assert data['jsonrpc'] == '2.0'
        assert data['result'] == 'pong'
        assert data['id'] == 1
    finally:
        server.stop()


def test_server_http_invalid_json():
    """Test that server handles invalid JSON gracefully."""
    port = find_free_port()
    server = MCPServer(host='localhost', port=port)

    # Start server in background thread
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(0.5)

    try:
        # Send invalid JSON
        request_data = b'not valid json'
        request = Request(
            f'http://localhost:{port}',
            data=request_data,
            headers={'Content-Type': 'application/json'}
        )
        response = urlopen(request, timeout=2)

        assert response.status == 200
        data = json.loads(response.read().decode('utf-8'))
        assert data['jsonrpc'] == '2.0'
        assert 'error' in data
        assert data['error']['code'] == -32700
        assert 'Parse error' in data['error']['message']
    finally:
        server.stop()


def test_server_http_custom_method():
    """Test that server handles custom methods over HTTP."""
    port = find_free_port()
    server = MCPServer(host='localhost', port=port)

    # Register custom method
    def echo_handler(request):
        return request.get('params', {})

    server.register_method('echo', echo_handler)

    # Start server in background thread
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Wait for server to start
    time.sleep(0.5)

    try:
        # Send custom method request
        request_data = json.dumps({
            'jsonrpc': '2.0',
            'method': 'echo',
            'params': {'message': 'hello world'},
            'id': 7
        }).encode('utf-8')
        request = Request(
            f'http://localhost:{port}',
            data=request_data,
            headers={'Content-Type': 'application/json'}
        )
        response = urlopen(request, timeout=2)

        assert response.status == 200
        data = json.loads(response.read().decode('utf-8'))
        assert data['jsonrpc'] == '2.0'
        assert data['result']['message'] == 'hello world'
        assert data['id'] == 7
    finally:
        server.stop()


def test_server_initialization_with_custom_host_port():
    """Test that server can be initialized with custom host and port."""
    server = MCPServer(host='127.0.0.1', port=9999)
    assert server.host == '127.0.0.1'
    assert server.port == 9999
    assert server.running is False
    assert len(server.custom_methods) == 0
