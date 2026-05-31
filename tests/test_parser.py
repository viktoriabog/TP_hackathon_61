import pytest
import json
import tempfile
import os
from app.parsers.txt_parser import TxtParser
from app.parsers.json_parser import JsonParser
from app.parsers.email_parser import EmailParser


@pytest.fixture
def txt_parser():
    return TxtParser()


@pytest.fixture
def json_parser():
    return JsonParser()


@pytest.fixture
def email_parser():
    return EmailParser()


def write_temp_file(content, suffix=".txt", encoding="utf-8"):
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, encoding=encoding, delete=False
    )
    f.write(content)
    f.close()
    return f.name




def test_txt_parser_reads_subject(txt_parser):
    path = write_temp_file("From: user@test.com\nSubject: Тест письма\n\nТело письма")
    email = txt_parser.parse(path)
    assert email.subject == "Тест письма"
    os.unlink(path)


def test_txt_parser_reads_sender_plain(txt_parser):
    path = write_temp_file("From: user@test.com\nSubject: Тест\n\nТело")
    email = txt_parser.parse(path)
    assert email.sender == "user@test.com"
    os.unlink(path)


def test_txt_parser_reads_sender_angle_brackets(txt_parser):
    path = write_temp_file("From: Иван Иванов <ivan@test.com>\nSubject: Тест\n\nТело")
    email = txt_parser.parse(path)
    assert email.sender == "ivan@test.com"
    os.unlink(path)


def test_txt_parser_russian_headers(txt_parser):
    path = write_temp_file("От кого: test@test.com\nТема: Проверка\n\nТело")
    email = txt_parser.parse(path)
    assert email.subject == "Проверка"
    assert email.sender == "test@test.com"
    os.unlink(path)


def test_txt_parser_missing_headers_defaults(txt_parser):
    path = write_temp_file("Просто текст без заголовков")
    email = txt_parser.parse(path)
    assert email.sender == "unknown"
    assert email.subject == ""
    os.unlink(path)


def test_txt_parser_body_contains_full_content(txt_parser):
    content = "From: a@b.com\nSubject: X\n\nТело письма здесь"
    path = write_temp_file(content)
    email = txt_parser.parse(path)
    assert "Тело письма здесь" in email.body
    os.unlink(path)




def test_json_parser_reads_all_fields(json_parser):
    data = {"subject": "Тема", "body": "Тело", "sender": "s@s.com"}
    path = write_temp_file(json.dumps(data), suffix=".json")
    email = json_parser.parse(path)
    assert email.subject == "Тема"
    assert email.body == "Тело"
    assert email.sender == "s@s.com"
    os.unlink(path)


def test_json_parser_missing_fields_defaults(json_parser):
    path = write_temp_file("{}", suffix=".json")
    email = json_parser.parse(path)
    assert email.subject == ""
    assert email.body == ""
    assert email.sender == ""
    os.unlink(path)




def test_email_parser_routes_txt(email_parser):
    path = write_temp_file("From: a@b.com\nSubject: X\n\nТело", suffix=".txt")
    email = email_parser.parse(path)
    assert email.subject == "X"
    os.unlink(path)


def test_email_parser_routes_json(email_parser):
    path = write_temp_file(
        json.dumps({"subject": "JS", "body": "тело", "sender": "a@b.com"}),
        suffix=".json"
    )
    email = email_parser.parse(path)
    assert email.subject == "JS"
    os.unlink(path)


def test_email_parser_unsupported_format_raises(email_parser):
    with pytest.raises(ValueError, match="Unsupported file format"):
        email_parser.parse("file.bin")
