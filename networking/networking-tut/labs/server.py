#!/usr/bin/env python3
"""Loopback-only HTTP teaching service. No external requests or API credentials."""
import argparse
import json
import math
import threading
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


class LabServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address):
        super().__init__(address, Handler)
        self.lock = threading.Lock()
        self.attempts = Counter()
        self.completed = Counter()


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    server_version = 'NetworkingLab/1.0'

    def log_message(self, fmt, *args):
        # Avoid noisy traces when an experiment deliberately closes its client.
        pass

    def reply(self, status, body, headers=None):
        payload = json.dumps(body).encode()
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            for name, value in (headers or {}).items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def do_GET(self):
        url = urlsplit(self.path)
        query = parse_qs(url.query)
        key = query.get('key', ['demo'])[0][:100]
        if url.path == '/ok':
            return self.reply(200, {'outcome': 'complete', 'answer': 'Hello from the local lab.'})
        if url.path == '/status/429':
            return self.reply(429, {'error': 'simulated_rate_limit', 'note': 'Always 429 for teaching; waiting will not clear this endpoint.'}, {'Retry-After': '2'})
        if url.path == '/flaky':
            with self.server.lock:
                self.server.attempts[key] += 1
                attempt = self.server.attempts[key]
            return self.reply(503 if attempt == 1 else 200, {'attempt': attempt, 'outcome': 'unavailable' if attempt == 1 else 'complete'}, {'Retry-After': '1'} if attempt == 1 else None)
        if url.path == '/slow':
            try:
                delay = float(query.get('seconds', ['3'])[0])
                if not math.isfinite(delay) or not 0 <= delay <= 10:
                    raise ValueError
            except ValueError:
                return self.reply(400, {'error': 'seconds must be a finite number between 0 and 10'})
            time.sleep(delay)
            with self.server.lock:
                self.server.completed[key] += 1
            return self.reply(200, {'outcome': 'complete', 'key': key, 'delay_seconds': delay})
        if url.path == '/stats':
            with self.server.lock:
                snapshot = {'flaky_attempts': dict(self.server.attempts), 'slow_completed': dict(self.server.completed)}
            return self.reply(200, snapshot)
        if url.path == '/stream':
            cut = query.get('cut', ['0'])[0] == '1'
            self.close_connection = True
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Connection', 'close')
                self.end_headers()
                for token in ['Networks', ' move', ' bytes.']:
                    self.wfile.write(('event: token\ndata: ' + json.dumps({'text': token}) + '\n\n').encode())
                    self.wfile.flush()
                    time.sleep(0.25)
                    if cut:
                        return
                self.wfile.write(b'event: done\ndata: {"complete": true}\n\n')
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        return self.reply(404, {'error': 'unknown_path', 'paths': ['/ok', '/status/429', '/slow', '/flaky', '/stream', '/stats']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = LabServer(('127.0.0.1', args.port))
    print(f'Lab listening at http://127.0.0.1:{server.server_port}', flush=True)
    print('Stop with Ctrl-C. All state is in memory and resets on restart.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
