"""Shared launcher utilities for OpenSeismo startup flows."""

from __future__ import annotations

import logging
import socket
import threading
import time
import webbrowser
from pathlib import Path
from typing import Callable


class DesktopLauncher:
    """Controlled desktop startup flow for OpenSeismo."""

    def __init__(
        self,
        app_name: str,
        url: str,
        run_app: Callable[..., None],
        host: str,
        port: int,
        lock_name: str = 'OpenSeismoLite.lock',
        browser_delay: float = 2.0,
    ) -> None:
        self.app_name = app_name
        self.url = url
        self.run_app = run_app
        self.host = host
        self.port = port
        self.lock_name = lock_name
        self.browser_delay = browser_delay
        self.lock_file: Path | None = None

    def get_lock_file(self) -> Path:
        temp_dir = Path(__import__('os').environ.get('TEMP', '/tmp'))
        return temp_dir / self.lock_name

    def acquire_lock(self) -> bool:
        self.lock_file = self.get_lock_file()

        if self.lock_file.exists():
            try:
                with open(self.lock_file, 'r') as f:
                    old_pid = f.read().strip()
                    import time as time_module
                    file_age = time_module.time() - self.lock_file.stat().st_mtime
                    if file_age > 10:
                        self.lock_file.unlink()
            except Exception:
                pass

        if not self.lock_file.exists():
            try:
                with open(self.lock_file, 'w') as f:
                    f.write(str(__import__('os').getpid()))
                return True
            except Exception:
                return False

        return False

    def cleanup_lock(self) -> None:
        if self.lock_file and self.lock_file.exists():
            try:
                self.lock_file.unlink()
            except Exception:
                pass

    def is_port_in_use(self, timeout: float = 1.0) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                return s.connect_ex((self.host, self.port)) == 0
        except Exception:
            return False

    def open_browser_delayed(self) -> None:
        time.sleep(self.browser_delay)
        try:
            webbrowser.open(self.url)
        except Exception as exc:
            logging.getLogger(__name__).warning('Browser launch failed: %s', exc)

    def run(self) -> None:
        if not self.acquire_lock():
            print(f'{self.app_name} is already running.')
            print(f'Connecting to {self.url}')
            time.sleep(1)
            webbrowser.open(self.url)
            return

        try:
            if self.is_port_in_use():
                print(f'{self.app_name} is already running on {self.url}')
                webbrowser.open(self.url)
                return

            print(f'Starting {self.app_name}...')
            print(f'Launching server on {self.url}')

            browser_thread = threading.Thread(target=self.open_browser_delayed, daemon=True)
            browser_thread.start()

            self.run_app(host=self.host, port=self.port, debug=False)
        finally:
            self.cleanup_lock()


def is_port_in_use(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except Exception:
        return False


def wait_for_server(host: str, port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_in_use(host, port, timeout=0.25):
            return True
        time.sleep(0.1)
    return False
