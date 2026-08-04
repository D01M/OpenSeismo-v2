from pathlib import Path

from openseismo import config
import run_desktop


def test_flask_host_allows_localhost_access():
    assert config.FLASK_HOST == "0.0.0.0"


def test_acquire_lock_recovers_from_dead_process(tmp_path, monkeypatch):
    lock_file = tmp_path / "OpenSeismoLite.lock"
    lock_file.write_text("999999999", encoding="utf-8")

    monkeypatch.setattr(run_desktop, "get_lock_file", lambda: lock_file)

    assert run_desktop.acquire_lock() is True
    assert lock_file.exists()
    assert lock_file.read_text(encoding="utf-8") == str(run_desktop.os.getpid())
