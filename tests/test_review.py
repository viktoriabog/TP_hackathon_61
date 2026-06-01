import json
from pathlib import Path
from unittest.mock import patch

from review_unknown import review, extract_keywords, load_categories, save_categories


def test_extract_keywords_basic():
    text = "Настроить VPN"

    result = extract_keywords(text)

    assert "настроить" in result


def test_load_categories_empty(tmp_path, monkeypatch):
    fake_config = tmp_path / "config" / "categories.json"

    monkeypatch.setattr("review_unknown.CONFIG_PATH", fake_config)

    result = load_categories()

    assert result == {}


def test_save_categories(tmp_path, monkeypatch):
    fake_config = tmp_path / "config" / "categories.json"

    monkeypatch.setattr("review_unknown.CONFIG_PATH", fake_config)

    save_categories({"it_support": ["vpn"]})

    assert fake_config.exists()

    data = json.loads(fake_config.read_text(encoding="utf-8"))
    assert "it_support" in data


def test_review_moves_file(tmp_path, monkeypatch, capsys):
    output = tmp_path / "output"
    unknown = output / "unknown"
    unknown.mkdir(parents=True)

    mail_file = unknown / "mail.txt"
    mail_file.write_text("Настроить VPN", encoding="utf-8")

    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True)

    config_file = config_dir / "categories.json"
    config_file.write_text(json.dumps({
        "it_support": []
    }), encoding="utf-8")

    monkeypatch.setattr("review_unknown.OUTPUT_DIR", output)
    monkeypatch.setattr("review_unknown.CONFIG_PATH", config_file)

    with patch("builtins.input", return_value="1"):
        review()

    captured = capsys.readouterr()

    assert "Перемещено" in captured.out
    assert (output / "it_support" / "mail.txt").exists()


def test_review_empty_unknown(tmp_path, monkeypatch, capsys):
    output = tmp_path / "output"
    unknown = output / "unknown"
    unknown.mkdir(parents=True)

    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True)

    config_file = config_dir / "categories.json"
    config_file.write_text(json.dumps({
        "it_support": []
    }), encoding="utf-8")

    monkeypatch.setattr("review_unknown.OUTPUT_DIR", output)
    monkeypatch.setattr("review_unknown.CONFIG_PATH", config_file)

    review()

    captured = capsys.readouterr()

    assert "Нет неизвестных писем" in captured.out
