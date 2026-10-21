import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "download_data.py"

spec = importlib.util.spec_from_file_location("download_data", SCRIPT_PATH)
download_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(download_data)


def test_empty_download_is_rejected_and_temporary_file_removed(
    tmp_path, monkeypatch
):
    destination = tmp_path / "data.csv"

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size):
            yield b""

    monkeypatch.setattr(
        download_data.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    with pytest.raises(ValueError, match="empty"):
        download_data.download("https://example.com/data.csv", destination)

    assert not destination.exists()
    assert not destination.with_name("data.csv.part").exists()


def test_http_error_removes_temporary_file(tmp_path, monkeypatch):
    destination = tmp_path / "data.csv"

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def raise_for_status(self):
            raise download_data.requests.HTTPError("404 Not Found")

    monkeypatch.setattr(
        download_data.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    with pytest.raises(download_data.requests.HTTPError):
        download_data.download("https://example.com/missing.csv", destination)

    assert not destination.exists()
    assert not destination.with_name("data.csv.part").exists()
    