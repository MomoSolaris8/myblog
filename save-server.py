#!/usr/bin/env python3
"""
Local save server — runs on port 4001
Receives POST /save-post and writes the file directly into _posts/
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, pathlib

POSTS_DIR = pathlib.Path(__file__).parent / '_posts'

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path == '/save-post':
            length = int(self.headers.get('Content-Length', 0))
            body   = json.loads(self.rfile.read(length))
            dest   = POSTS_DIR / body['filename']
            dest.write_text(body['content'], encoding='utf-8')
            print(f"  saved → _posts/{body['filename']}")
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, *_):
        pass  # silence default request logs

if __name__ == '__main__':
    server = HTTPServer(('localhost', 4001), Handler)
    print('Save server ready on :4001')
    server.serve_forever()
