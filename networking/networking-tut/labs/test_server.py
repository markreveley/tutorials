"""Protocol-level checks for the course experiments; Python standard library only."""
import http.client
import json
import socket
import threading
import time
import unittest
from server import LabServer


class LabChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LabServer(('127.0.0.1', 0))
        cls.thread = threading.Thread(target=cls.server.serve_forever, kwargs={'poll_interval': .02}, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, timeout=2):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=timeout)
        try:
            connection.request('GET', path)
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read().decode()
        finally:
            connection.close()

    def test_success_and_missing_route(self):
        status, _, body = self.request('/ok')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['outcome'], 'complete')
        self.assertEqual(self.request('/missing')[0], 404)

    def test_rate_limit_with_retry_hint(self):
        status, headers, _ = self.request('/status/429')
        self.assertEqual((status, headers['Retry-After']), (429, '2'))

    def test_transient_failure_then_success(self):
        self.assertEqual(self.request('/flaky?key=test-retry')[0], 503)
        status, _, body = self.request('/flaky?key=test-retry')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['attempt'], 2)

    def test_stream_completion_is_separate_from_http_success(self):
        for path, completed in [('/stream', True), ('/stream?cut=1', False)]:
            status, headers, body = self.request(path)
            self.assertEqual(status, 200)
            self.assertEqual(headers['Content-Type'], 'text/event-stream')
            self.assertEqual('event: done' in body, completed)
            self.assertIn('event: token', body)

    def test_remote_work_survives_client_timeout(self):
        with self.assertRaises((TimeoutError, socket.timeout)):
            self.request('/slow?seconds=0.15&key=lost-response', timeout=.03)
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            _, _, body = self.request('/stats')
            if json.loads(body)['slow_completed'].get('lost-response') == 1:
                break
            time.sleep(.02)
        else:
            self.fail('Server work did not complete after the caller timed out')

    def test_delay_input_validation(self):
        for value in ('nan', 'inf', '-1', '11', 'garbage'):
            self.assertEqual(self.request('/slow?seconds='+value)[0], 400)


if __name__ == '__main__':
    unittest.main()
