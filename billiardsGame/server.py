import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Specify the file you want to serve
        filename = 'pool-table.html'  # Change 'index.html' to your file's name

        if self.path == '/pool-table.html':
            try:
                # Attempt to open the specified HTML file
                with open(filename, 'rb') as file:
                    content = file.read()
                # Send HTTP response headers
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-length', len(content))
                self.end_headers()
                # Write the content of the file to the response
                self.wfile.write(content)
            except FileNotFoundError:
                # File not found; send 404 response
                self.send_error(404, f'File {filename} not found')
        else:
            # Path does not match the specified file; send 404 response
            self.send_error(404, 'File not found')

# Main block to run the server
if __name__ == '__main__':
    port = 59167  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # Use the provided argument as the port
        except ValueError:
            print("Usage: python server.py [port]")

    try:
        # Set up and start the HTTP server
        httpd = HTTPServer(('localhost', port), MyHandler)
        print(f'Server listening on port: {port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Handle Ctrl+C to stop the server
        print('\nServer stopped')
        httpd.server_close()
