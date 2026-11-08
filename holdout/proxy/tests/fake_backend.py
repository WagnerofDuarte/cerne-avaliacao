"""Backend FALSO para testar o addon (nunca o backend hospedado)."""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class Fake(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    recebidos = []  # cabecalhos e caminhos recebidos

    def log_message(self, *a):
        pass

    def _send(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        self.do_GET()

    def do_GET(self):
        u = urlparse(self.path)
        fn = u.path.rsplit("/", 1)[-1]
        Fake.recebidos.append({"fn": fn, "path": self.path, "headers": {k.lower(): v for k, v in self.headers.items()}})
        if self.headers.get("X-Test-Fault"):
            return self._send({"fault_visto": self.headers["X-Test-Fault"]}, 504)
        if fn == "chat-messages-send":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            for i in range(1, 7):
                ev = f"event: token\ndata: {{\"i\": {i}}}\n\n".encode()
                self.wfile.write(f"{len(ev):x}\r\n".encode() + ev + b"\r\n")
                self.wfile.flush()
                time.sleep(0.05)
            ev = b"event: done\ndata: {}\n\n"
            self.wfile.write(f"{len(ev):x}\r\n".encode() + ev + b"\r\n0\r\n\r\n")
            return
        if fn == "dashboard-narrative-get":
            return self._send({"narrative": "texto original", "chart": [1, 2]})
        if fn == "export-status-get":
            return self._send({"status": "done", "downloadAvailable": True})
        self._send({"ok": True, "fn": fn, "q": parse_qs(u.query)})


def iniciar(porta=0):
    srv = ThreadingHTTPServer(("127.0.0.1", porta), Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv
