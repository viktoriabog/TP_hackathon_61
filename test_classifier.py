from app.classifiers.keyword_classifier import KeywordClassifier
from app.models.email import Email


def test_classifier():

    email = Email(
        subject="VPN issue",
        body="Не работает пароль",
        sender="employee@test.com",
        filepath="mail.txt"
    )

    classifier = KeywordClassifier()

    category, confidence = classifier.classify(email)

    assert category == "access_management"