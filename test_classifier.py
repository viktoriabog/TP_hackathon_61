from app.classifiers.keyword_classifier import KeywordClassifier
from app.models.email import Email


email = Email(
    subject="Не работает VPN",
    body="После смены пароля не могу войти",
    sender="employee@company.com",
    filepath="mail_1.txt"
)

classifier = KeywordClassifier()

result = classifier.classify(email)

print(result)