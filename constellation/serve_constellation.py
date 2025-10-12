#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick web server for constellation explorer
Run this and open http://localhost:8000/constellation_explorer.html
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    Handler = MyHTTPRequestHandler

    print(f"\n*** Starting Constellation Explorer Server ***\n")
    print(f"   Server running at: http://localhost:{PORT}")
    print(f"   Opening browser...\n")
    print(f"   Press Ctrl+C to stop\n")

    # Open browser
    webbrowser.open(f'http://localhost:{PORT}/constellation_explorer.html')

    # Start server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n*** Server stopped. Constellation remains alive in memory.\n")
