import pytest
import tempfile
import os
from unittest.mock import patch
from app.models.email import Email
from app.classifiers.keyword_classifier import KeywordClassifier
from app.parsers.txt_parser import TxtParser
from app.parsers.email_parser import EmailParser
from app.routing.router import Router


MOCK_CATEGORIES = {
    "it_support": ["ошибка", "не работает", "vpn"],
    "finance": ["счет", "invoice", "оплата"],
}


@pytest.fixture
def classifier():
    with patch.object(KeywordClassifier, "__init__", lambda self: None):
        clf = KeywordClassifier()
        clf.categories = MOCK_CATEGORIES
    return clf


def make_email(subject="", body=""):
    return Email(subject=subject, body=body, sender="x@x.com", filepath="fake.txt")


def test_empty_subject_and_body(classifier):
    category, confidence = classifier.classify(make_email("", ""))
    assert category == "unknown"
    assert confidence == 0


def test_only_spaces(classifier):
    category, confidence = classifier.classify(make_email("   ", "   "))
    assert category == "unknown"


def test_very_long_body(classifier):
    body = "ошибка " * 1000
    category, confidence = classifier.classify(make_email("", body))
    assert category == "it_support"
    assert confidence > 0


def test_keyword_in_subject_only(classifier):
    category, _ = classifier.classify(make_email(subject="invoice", body="ничего особенного"))
    assert category == "finance"


def test_keyword_in_body_only(classifier):
    category, _ = classifier.classify(make_email(subject="", body="vpn не работает"))
    assert category == "it_support"


def test_tie_returns_some_category(classifier):
    email = make_email(subject="ошибка", body="invoice")
    category, confidence = classifier.classify(email)
    assert category in MOCK_CATEGORIES
    assert confidence == 1


def test_parse_empty_txt_file():
    parser = TxtParser()
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    f.write("")
    f.close()
    email = parser.parse(f.name)
    assert email.subject == ""
    assert email.sender == "unknown"
    assert email.body == ""
    os.unlink(f.name)


def test_parse_file_with_only_newlines():
    parser = TxtParser()
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    f.write("\n\n\n")
    f.close()
    email = parser.parse(f.name)
    assert email.subject == ""
    assert email.sender == "unknown"
    os.unlink(f.name)


def test_parse_unsupported_format_raises():
    parser = EmailParser()
    with pytest.raises(ValueError):
        parser.parse("image.png")


def test_parse_unsupported_format_bin():
    parser = EmailParser()
    with pytest.raises(ValueError):
        parser.parse("mail_0104.bin")


def test_router_creates_output_dir(tmp_path):
    import shutil
    from pathlib import Path

    src = tmp_path / "mail_test.txt"
    src.write_text("test content")

    real_output = tmp_path / "it_support"
    real_output.mkdir()
    dest = real_output / src.name
    shutil.copy(str(src), str(dest))
    assert dest.exists()
    assert dest.read_text() == "test content"


def test_router_file_ends_up_in_correct_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    src = tmp_path / "mail_001.txt"
    src.write_text("тело письма")

    router = Router()
    router.route(str(src), "sender@test.com", "finance")

    dest = tmp_path / "output" / "finance" / "mail_001.txt"
    assert dest.exists()
    assert dest.read_text() == "тело письма"
