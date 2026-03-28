"""MCP (Model Context Protocol) server for AgenticStarter."""

import json
import signal
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Callable, Optional


class MCPServer:
    """Minimal Model Context Protocol server with agentic execution embed support."""

    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.running = False
        self.server: Optional[HTTPServer] = None
        self.custom_methods: Dict[str, Callable] = {}

    def register_method(self, method_name: str, handler: Callable) -> None:
        """
        Register a custom method for agentic execution embed.

        Args:
            method_name: Name of the method to register
            handler: Callable that takes request dict and returns result
        """
        self.custom_methods[method_name] = handler

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle JSON-RPC 2.0 request.

        Args:
            request: JSON-RPC request dictionary

        Returns:
            JSON-RPC response dictionary
        """
        # Validate JSON-RPC 2.0 format
        if not isinstance(request, dict):
            return {
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32600,
                    'message': 'Invalid Request'
                }
            }

        if request.get('jsonrpc') != '2.0':
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32600,
                    'message': 'Invalid Request: jsonrpc version must be 2.0'
                }
            }

        method = request.get('method')
        if not method:
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32600,
                    'message': 'Invalid Request: method is required'
                }
            }

        # Handle built-in ping method
        if method == 'ping':
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'result': 'pong'
            }

        # Handle custom methods (agentic execution embed)
        if method in self.custom_methods:
            try:
                result = self.custom_methods[method](request)
                return {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': result
                }
            except Exception as e:
                return {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'error': {
                        'code': -32603,
                        'message': f'Internal error: {str(e)}'
                    }
                }

        # Method not found
        return {
            'jsonrpc': '2.0',
            'id': request.get('id'),
            'error': {
                'code': -32601,
                'message': 'Method not found'
            }
        }

    def start(self):
        """Start the MCP server."""
        self.running = True

        # Create request handler with reference to this server instance
        mcp_server_instance = self

        class MCPRequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress default logging."""
                pass

            def do_POST(self):
                """Handle POST requests with JSON-RPC 2.0 messages."""
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)

                    # Parse JSON request
                    try:
                        request = json.loads(body.decode('utf-8'))
                    except json.JSONDecodeError:
                        response = {
                            'jsonrpc': '2.0',
                            'id': None,
                            'error': {
                                'code': -32700,
                                'message': 'Parse error'
                            }
                        }
                        self.send_response_json(response)
                        return

                    # Handle request using MCPServer instance
                    response = mcp_server_instance.handle_request(request)
                    self.send_response_json(response)

                except Exception as e:
                    error_response = {
                        'jsonrpc': '2.0',
                        'id': None,
                        'error': {
                            'code': -32603,
                            'message': f'Internal error: {str(e)}'
                        }
                    }
                    self.send_response_json(error_response)

            def send_response_json(self, response_data):
                """Send JSON response."""
                response_body = json.dumps(response_data).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)

        # Create and start HTTP server
        self.server = HTTPServer((self.host, self.port), MCPRequestHandler)
        self.server.timeout = 0.5  # Allow checking running flag periodically

        # Setup signal handlers for graceful shutdown (only in main thread)
        try:
            def signal_handler(sig, frame):
                print("\nShutting down MCP server...")
                self.stop()
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
        except ValueError:
            # Signal handlers can only be set in main thread
            pass

        print(f"MCP Server listening on {self.host}:{self.port}")
        print("Ready to handle JSON-RPC 2.0 requests")
        print("Press Ctrl+C to stop")

        # Start serving with periodic checks
        try:
            while self.running:
                self.server.handle_request()
        except KeyboardInterrupt:
            pass
        finally:
            if self.running:  # Only print if we're actually stopping
                self.running = False
                if self.server:
                    self.server.server_close()
                print("MCP Server stopped")

    def stop(self):
        """Stop the MCP server."""
        self.running = False
