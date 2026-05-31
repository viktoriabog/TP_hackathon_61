import pytest
from unittest.mock import patch
from app.models.email import Email
from app.classifiers.keyword_classifier import KeywordClassifier


MOCK_CATEGORIES = {
    "it_support": ["ошибка", "не работает", "сбой", "vpn"],
    "finance": ["счет", "invoice", "оплата", "платеж"],
    "hr": ["отпуск", "больничный", "вакансия", "hr"],
    "spam_phishing": ["выигрыш", "подарок", "срочно подтвердите"],
    "monitoring_alerts": ["[warning]", "[error]", "alert", "cpu"],
}


@pytest.fixture
def classifier():
    with patch.object(KeywordClassifier, "__init__", lambda self: None):
        clf = KeywordClassifier()
        clf.categories = MOCK_CATEGORIES
    return clf


def make_email(subject="", body=""):
    return Email(subject=subject, body=body, sender="test@test.com", filepath="fake.txt")


def test_classify_it_support(classifier):
    email = make_email(subject="Ошибка при входе", body="VPN не работает с утра")
    category, confidence = classifier.classify(email)
    assert category == "it_support"
    assert confidence > 0


def test_classify_finance(classifier):
    email = make_email(subject="Invoice #123", body="Прошу подтвердить оплату счета")
    category, confidence = classifier.classify(email)
    assert category == "finance"
    assert confidence > 0


def test_classify_hr(classifier):
    email = make_email(subject="Заявление на отпуск", body="Прошу предоставить отпуск с 1 июня")
    category, confidence = classifier.classify(email)
    assert category == "hr"
    assert confidence > 0


def test_classify_spam(classifier):
    email = make_email(subject="Вы выиграли!", body="Срочно подтвердите получение подарка")
    category, confidence = classifier.classify(email)
    assert category == "spam_phishing"
    assert confidence > 0


def test_classify_monitoring(classifier):
    email = make_email(subject="[WARNING] CPU high", body="alert: cpu usage 95%")
    category, confidence = classifier.classify(email)
    assert category == "monitoring_alerts"
    assert confidence > 0


def test_classify_unknown_returns_unknown(classifier):
    email = make_email(subject="Привет", body="Как дела? Всё хорошо.")
    category, confidence = classifier.classify(email)
    assert category == "unknown"
    assert confidence == 0


def test_classify_empty_email(classifier):
    email = make_email(subject="", body="")
    category, confidence = classifier.classify(email)
    assert category == "unknown"
    assert confidence == 0


def test_classify_case_insensitive(classifier):
    email = make_email(subject="ОШИБКА", body="VPN НЕ РАБОТАЕТ")
    category, confidence = classifier.classify(email)
    assert category == "it_support"


def test_classify_returns_best_match(classifier):
    email = make_email(subject="Отпуск", body="счет invoice оплата")
    category, confidence = classifier.classify(email)
    assert category == "finance"
    assert confidence == 3


@pytest.mark.parametrize("subject,body,expected", [
    ("Сбой системы", "ошибка при запуске vpn", "it_support"),
    ("Invoice due", "платеж просрочен", "finance"),
    ("Больничный лист", "hr отдел", "hr"),
    ("[ERROR] disk full", "alert cpu", "monitoring_alerts"),
    ("Выигрыш!", "подарок ждёт", "spam_phishing"),
])
def test_classify_parametrized(classifier, subject, body, expected):
    email = make_email(subject=subject, body=body)
    category, _ = classifier.classify(email)
    assert category == expected
