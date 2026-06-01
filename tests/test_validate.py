import pytest
import json
from pathlib import Path

from validate import validate


def test_validate_success(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    (inbox / "mail.txt").write_text("hello")

    config = tmp_path / "categories.json"
    config.write_text(json.dumps({
        "finance": ["оплата"],
        "unknown": []
    }), encoding="utf-8")

    assert validate(
        inbox_dir=str(inbox),
        config_path=str(config)
    ) is True


def test_validate_missing_inbox(tmp_path):
    config = tmp_path / "categories.json"
    config.write_text(json.dumps({"finance": ["оплата"]}))

    assert validate(
        inbox_dir=str(tmp_path / "inbox"),
        config_path=str(config)
    ) is False


def test_validate_missing_config(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    assert validate(
        inbox_dir=str(inbox),
        config_path=str(tmp_path / "categories.json")
    ) is False


def test_validate_invalid_json(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    config = tmp_path / "categories.json"
    config.write_text("{ finance: [] }")  # invalid JSON

    assert validate(
        inbox_dir=str(inbox),
        config_path=str(config)
    ) is False


def test_validate_warning_empty_inbox(tmp_path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()

    config = tmp_path / "categories.json"
    config.write_text(json.dumps({
        "finance": ["оплата"]
    }))

    assert validate(
        inbox_dir=str(inbox),
        config_path=str(config)
    ) is True