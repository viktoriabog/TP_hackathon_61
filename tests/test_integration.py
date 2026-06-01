import pytest
import tempfile
import shutil
from pathlib import Path

from app.parsers.email_parser import EmailParser
from app.classifiers.keyword_classifier import KeywordClassifier
from app.routing.router import Router
from app.utils.logger import Logger


def test_full_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        inbox = tmp_path / "inbox"
        output = tmp_path / "output"
        config_dir = tmp_path / "config"
        inbox.mkdir()
        output.mkdir()
        config_dir.mkdir()

        import json
        categories = {
            "finance": ["оплата", "счет", "зарплата"],
            "hr": ["отпуск", "больничный"],
            "unknown": []
        }
        (config_dir / "categories.json").write_text(
            json.dumps(categories, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        (inbox / "finance_letter.txt").write_text(
            "From: test@test.com\nSubject: Счет на оплату\n\nОплатите счет №123",
            encoding="utf-8"
        )
        (inbox / "hr_letter.txt").write_text(
            "From: hr@company.com\nSubject: Отпуск\n\nПрошу предоставить отпуск",
            encoding="utf-8"
        )
        (inbox / "unknown_letter.txt").write_text(
            "From: random@test.com\nSubject: Привет\n\nКак дела?",
            encoding="utf-8"
        )

        parser = EmailParser()
        classifier = KeywordClassifier()
        router = Router()
        logger = Logger()

        original_cwd = Path.cwd()
        import os
        os.chdir(tmp_path)

        try:
            for filepath in inbox.iterdir():
                try:
                    email = parser.parse(str(filepath))
                    category, _ = classifier.classify(email)
                    router.route(str(filepath), email.sender, category)
                    logger.info(f"{filepath.name} -> {category}")
                except Exception as e:
                    logger.error(f"{filepath.name}: {e}")

            output_path = tmp_path / "output"
            assert (output_path / "finance" / "finance_letter.txt").exists()
            assert (output_path / "hr" / "hr_letter.txt").exists()
            assert (output_path / "unknown" / "unknown_letter.txt").exists()

        finally:
            os.chdir(original_cwd)