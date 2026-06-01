import pytest
import tempfile
import shutil
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture
def temp_project():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        (tmp_path / "inbox").mkdir()
        (tmp_path / "output").mkdir()
        (tmp_path / "config").mkdir()

        real_config = Path("config/categories.json")
        if real_config.exists():
            shutil.copy(real_config, tmp_path / "config" / "categories.json")
        else:
            minimal_cats = {
                "finance": ["оплата", "счет", "зарплата", "invoice"],
                "hr": ["отпуск", "больничный", "кадры", "hr"],
                "it_support": ["ошибка", "не работает", "vpn", "сбой"],
                "unknown": []
            }
            (tmp_path / "config" / "categories.json").write_text(
                json.dumps(minimal_cats, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        yield tmp_path


@pytest.fixture
def temp_project_with_emails(temp_project):
    inbox = temp_project / "inbox"
    (inbox / "finance_letter.txt").write_text(
        "From: test@test.com\nSubject: Счет на оплату\n\nПрошу оплатить счет №123",
        encoding="utf-8"
    )

    (inbox / "hr_letter.txt").write_text(
        "From: hr@company.com\nSubject: Отпуск\n\nХочу взять отпуск в июне",
        encoding="utf-8"
    )

    (inbox / "it_letter.txt").write_text(
        "From: user@office.com\nSubject: Ошибка VPN\n\nVPN не работает, срочно помогите",
        encoding="utf-8"
    )

    (inbox / "random_letter.txt").write_text(
        "From: friend@home.com\nSubject: Привет\n\nКак дела?",
        encoding="utf-8"
    )
    return temp_project
