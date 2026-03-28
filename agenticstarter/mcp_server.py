"""
MCP Server implementation for AgenticStarter (Feature 3)

Provides a minimal Model Context Protocol server with JSON-RPC 2.0 support
and extensibility via tool registration for agentic execution.
"""

import json
import threading
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Dict, Any, Optional


class ReuseAddrHTTPServer(HTTPServer):
    """HTTPServer that allows address reuse."""
    allow_reuse_address = True


class MCPServer:
    """
    Minimal Model Context Protocol server.

    Handles JSON-RPC 2.0 requests and supports agentic execution via
    custom tool registration.
    """

    def __init__(self, host: str = "localhost", port: int = 8000):
        """
        Initialize the MCP server.

        Args:
            host: Host address to bind to (default: localhost)
            port: Port number to listen on (default: 8000)
        """
        self.host = host
        self.port = port
        self.tools: Dict[str, Callable] = {}
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None

    def register_tool(self, name: str, handler: Callable) -> None:
        """
        Register a custom tool for agentic execution.

        Args:
            name: Name of the tool (used as JSON-RPC method name)
            handler: Callable that implements the tool logic
        """
        self.tools[name] = handler

    def _handle_ping(self, params: Any) -> str:
        """Built-in ping handler."""
        return "pong"

    def _dispatch_method(self, method: str, params: Any) -> Any:
        """
        Dispatch a JSON-RPC method call.

        Args:
            method: Method name to call
            params: Parameters for the method

        Returns:
            Result of the method call

        Raises:
            ValueError: If method is not found
        """
        if method == "ping":
            return self._handle_ping(params)
        elif method in self.tools:
            return self.tools[method](params)
        else:
            raise ValueError(f"Method not found: {method}")

    def _create_request_handler(self):
        """Create a request handler class with access to server instance."""
        server_instance = self

        class MCPRequestHandler(BaseHTTPRequestHandler):
            """HTTP request handler for JSON-RPC 2.0 requests."""

            def log_message(self, format, *args):
                """Suppress default logging."""
                pass

            def do_POST(self):
                """Handle POST requests with JSON-RPC payloads."""
                try:
                    # Read request body
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)

                    # Parse JSON-RPC request
                    request = json.loads(body.decode('utf-8'))

                    # Validate JSON-RPC 2.0 format
                    if request.get('jsonrpc') != '2.0':
                        response = {
                            'jsonrpc': '2.0',
                            'error': {
                                'code': -32600,
                                'message': 'Invalid Request: jsonrpc version must be 2.0'
                            },
                            'id': request.get('id')
                        }
                    else:
                        method = request.get('method')
                        params = request.get('params')
                        request_id = request.get('id')

                        try:
                            # Dispatch method
                            result = server_instance._dispatch_method(method, params)
                            response = {
                                'jsonrpc': '2.0',
                                'result': result,
                                'id': request_id
                            }
                        except ValueError as e:
                            # Method not found
                            response = {
                                'jsonrpc': '2.0',
                                'error': {
                                    'code': -32601,
                                    'message': str(e)
                                },
                                'id': request_id
                            }
                        except Exception as e:
                            # Internal error
                            response = {
                                'jsonrpc': '2.0',
                                'error': {
                                    'code': -32603,
                                    'message': f'Internal error: {str(e)}'
                                },
                                'id': request_id
                            }

                    # Send response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))

                except json.JSONDecodeError:
                    # Parse error
                    response = {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32700,
                            'message': 'Parse error: Invalid JSON'
                        },
                        'id': None
                    }
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))

                except Exception as e:
                    # Server error
                    response = {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32000,
                            'message': f'Server error: {str(e)}'
                        },
                        'id': None
                    }
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))

        return MCPRequestHandler

    def start(self, blocking: bool = True) -> None:
        """
        Start the MCP server.

        Args:
            blocking: If True, run in current thread (blocks).
                     If False, run in background thread.
        """
        handler_class = self._create_request_handler()
        self.server = ReuseAddrHTTPServer((self.host, self.port), handler_class)
        self.server.allow_reuse_address = True

        if blocking:
            print(f"MCP Server listening on {self.host}:{self.port}")
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down MCP Server...")
                self.stop()
        else:
            # Run in background thread
            self.server_thread = threading.Thread(
                target=self.server.serve_forever,
                daemon=True
            )
            self.server_thread.start()

    def stop(self) -> None:
        """Stop the MCP server gracefully."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None

        if self.server_thread:
            self.server_thread.join(timeout=1.0)
            self.server_thread = None
