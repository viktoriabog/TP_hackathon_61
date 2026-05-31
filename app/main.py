from pathlib import Path

from app.parsers.email_parser import EmailParser
from app.classifiers.keyword_classifier import KeywordClassifier
from app.routing.router import Router
from app.utils.logger import Logger


class EmailProcessingPipeline:

    def __init__(self):

        self.parser = EmailParser()
        self.classifier = KeywordClassifier()
        self.router = Router()
        self.logger = Logger()

    def process_emails(self):

        inbox = Path("inbox")

        for filepath in inbox.iterdir():

            try:

                email = self.parser.parse(str(filepath))

                category, confidence = self.classifier.classify(email)

                self.router.route(
                    str(filepath),
                    email.sender,
                    category
                )

                self.logger.info(
                    f"{filepath.name} -> {category}"
                )

            except Exception as e:

                self.logger.error(
                    f"{filepath.name}: {e}"
                )


if __name__ == "__main__":

    pipeline = EmailProcessingPipeline()

    pipeline.process_emails()

    