#!/usr/bin/env python3
"""
Локальний сервер розробки з миттєвим оновленням (Live Reload) для папки dist/.
Не потребує встановлення жодних зовнішніх пакетів.

Запуск:
    python3 dev.py
    python3 dev.py --port 8000
"""

import argparse
import http.server
import json
import os
import posixpath
import queue
import socketserver
import threading
import time
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
LIVERELOAD_ENDPOINT = "/__livereload"

LIVERELOAD_SCRIPT = """
<script>
(() => {
  const SCROLL_KEY = '__dev_scroll_y';
  const savedY = sessionStorage.getItem(SCROLL_KEY);
  if (savedY !== null) {
    sessionStorage.removeItem(SCROLL_KEY);
    window.addEventListener('DOMContentLoaded', () => {
      window.scrollTo({ top: Number(savedY) || 0, behavior: 'instant' });
    });
  }

  let wasConnected = false;
  function connect() {
    const source = new EventSource('/__livereload');

    source.onopen = () => {
      if (wasConnected) {
        location.reload();
      }
      wasConnected = true;
    };

    source.addEventListener('change', (event) => {
      const data = JSON.parse(event.data);
      const changed = data.files || [];

      const onlyCss = changed.length > 0 && changed.every((f) => f.endsWith('.css'));
      if (onlyCss) {
        const stamp = Date.now();
        document.querySelectorAll('link[rel="stylesheet"]').forEach((link) => {
          const url = new URL(link.href, location.href);
          const relPath = decodeURIComponent(url.pathname).replace(/^\\//, '');
          if (!changed.includes(relPath) && !changed.includes('style.css')) return;
          url.searchParams.set('v', stamp);
          const clone = link.cloneNode();
          clone.href = url.toString();
          clone.onload = () => link.remove();
          link.after(clone);
        });
        return;
      }

      const onlyImages =
        changed.length > 0 &&
        changed.every((f) => /\\.(png|jpe?g|webp|gif|svg)$/i.test(f));
      if (onlyImages) {
        const stamp = Date.now();
        let updatedAny = false;
        document.querySelectorAll('img[src]').forEach((img) => {
          const url = new URL(img.src, location.href);
          const relPath = decodeURIComponent(url.pathname).replace(/^\\//, '');
          if (changed.includes(relPath)) {
            url.searchParams.set('v', stamp);
            img.src = url.toString();
            updatedAny = true;
          }
        });
        if (updatedAny) return;
      }

      sessionStorage.setItem(SCROLL_KEY, String(window.scrollY));
      location.reload();
    });

    source.onerror = () => {
      source.close();
      setTimeout(connect, 800);
    };
  }

  connect();
})();
</script>
"""


class ClientHub:
    """Зберігає підключених SSE-клієнтів та розсилає їм події змін файлів."""

    def __init__(self):
        self._lock = threading.Lock()
        self._clients: list[queue.Queue] = []

    def subscribe(self) -> queue.Queue:
        q: queue.Queue = queue.Queue()
        with self._lock:
            self._clients.append(q)
        return q

    def unsubscribe(self, q: queue.Queue) -> None:
        with self._lock:
            if q in self._clients:
                self._clients.remove(q)

    def broadcast(self, event: str, payload: dict) -> None:
        message = f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
        with self._lock:
            for q in list(self._clients):
                q.put(message)


def scan_files(directory: Path) -> dict[str, tuple[int, int]]:
    """Повертає словник {відносний_шлях: (mtime_ns, size)} для всіх файлів у проєкті."""
    snapshot: dict[str, tuple[int, int]] = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for name in files:
            full_path = Path(root) / name
            try:
                stat = full_path.stat()
                rel = full_path.relative_to(directory).as_posix()
                snapshot[rel] = (stat.st_mtime_ns, stat.st_size)
            except OSError:
                continue
    return snapshot


def watch_directory(directory: Path, hub: ClientHub, stop_event: threading.Event) -> None:
    """Відстежує зміни файлів у dist/ та сповіщає браузер."""
    prev = scan_files(directory)
    while not stop_event.wait(0.2):
        curr = scan_files(directory)
        if curr == prev:
            continue

        changed = [
            path for path, meta in curr.items() if prev.get(path) != meta
        ] + [
            path for path in prev if path not in curr
        ]
        prev = curr
        if changed:
            hub.broadcast("change", {"files": changed})


class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    hub: ClientHub

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == LIVERELOAD_ENDPOINT:
            self._handle_sse()
            return

        # Перевірка, чи запитується HTML-сторінка (для ін'єкції скрипта live reload)
        rel_path = urllib.parse.unquote(parsed.path.lstrip("/"))
        target = ROOT_DIR / (rel_path if rel_path else "index.html")
        if target.is_dir():
            target = target / "index.html"

        if target.is_file() and target.suffix.lower() in {".html", ".htm"}:
            self._serve_html_with_livereload(target)
            return

        super().do_GET()

    def _serve_html_with_livereload(self, file_path: Path) -> None:
        try:
            html = file_path.read_text(encoding="utf-8")
        except OSError:
            self.send_error(404, "File not found")
            return

        if "</body>" in html:
            html = html.replace("</body>", f"{LIVERELOAD_SCRIPT}\n</body>", 1)
        else:
            html += LIVERELOAD_SCRIPT

        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_sse(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        q = self.hub.subscribe()
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.flush()
            while True:
                try:
                    msg = q.get(timeout=15)
                    self.wfile.write(msg.encode("utf-8"))
                    self.wfile.flush()
                except queue.Empty:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            self.hub.unsubscribe(q)

    def log_message(self, format: str, *args) -> None:
        # Не засмічувати консоль частими SSE-підключеннями
        if args and LIVERELOAD_ENDPOINT in str(args[0]):
            return
        super().log_message(format, *args)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> None:
    parser = argparse.ArgumentParser(description="Live Reload dev server for dist/")
    parser.add_argument("--port", type=int, default=8000, help="Порт сервера (типово 8000)")
    args = parser.parse_args()

    if not ROOT_DIR.is_dir():
        raise SystemExit(f"Папку {ROOT_DIR} не знайдено.")

    hub = ClientHub()
    LiveReloadHandler.hub = hub

    stop_event = threading.Event()
    watcher = threading.Thread(
        target=watch_directory, args=(ROOT_DIR, hub, stop_event), daemon=True
    )
    watcher.start()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), LiveReloadHandler)
    print(f"Live Reload сервер запущено: http://localhost:{args.port}")
    print(f"Відстежуються зміни у: {ROOT_DIR}")
    print("Натисніть Ctrl+C для зупинки.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nЗупинка сервера...")
    finally:
        stop_event.set()
        server.server_close()


if __name__ == "__main__":
    main()
