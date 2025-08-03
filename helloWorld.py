import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Handle different routes
        if path == '/' or path == '/hello':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            html_response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Hello World Server</title>
            </head>
            <body>
                <h1>Hello World!</h1>
                <p>This is a simple Python HTTP server running without Flask or Django.</p>
                <p><a href="/api/hello">Try the JSON API endpoint</a></p>
            </body>
            </html>
            """
            self.wfile.write(html_response.encode('utf-8'))
            
        elif path == '/api/hello':
            # JSON API endpoint
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response_data = {
                "message": "Hello World!",
                "status": "success",
                "server": "Python built-in HTTP server"
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        else:
            # 404 for other paths
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1>')
    
    def log_message(self, format, *args):
        # Override to customize logging
        print(f"[{self.date_time_string()}] {format % args}")

def run_server():
    # Use PORT environment variable if available (for Render.com)
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'  # Bind to all interfaces for cloud deployment
    
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Server running on http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == '__main__':
    run_server()