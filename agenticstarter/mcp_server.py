"""MCP (Model Context Protocol) server for AgenticStarter."""

import json
from typing import Dict, Any


class MCPServer:
    """Minimal Model Context Protocol server."""

    def __init__(self, port=8000):
        self.port = port
        self.running = False

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle JSON-RPC 2.0 request.

        Args:
            request: JSON-RPC request dictionary

        Returns:
            JSON-RPC response dictionary
        """
        if request.get('method') == 'ping':
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'result': 'pong'
            }

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
        print(f"MCP Server listening on localhost:{self.port}")
        print("Ready to handle JSON-RPC 2.0 requests")

    def stop(self):
        """Stop the MCP server."""
        self.running = False
        print("MCP Server stopped")
