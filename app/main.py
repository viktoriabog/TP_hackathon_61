from pathlib import Path
import sys
from app.parsers.email_parser import EmailParser
from app.classifiers.keyword_classifier import KeywordClassifier
from app.routing.router import Router
from app.utils.logger import Logger
from collections import defaultdict
from validate import validate
import os
os.chdir(Path(__file__).parent.parent)
def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description="Автоматическая сортировка писем")
    parser.add_argument("--inbox", "-i", default="inbox", help="Папка с входящими письмами")
    parser.add_argument("--output", "-o", default="output", help="Папка для результатов")
    parser.add_argument("--config", "-c", default="config/categories.json", help="Файл категорий")
    parser.add_argument("--log", "-l", default="processing.log", help="Файл лога")
    return parser.parse_args()

class EmailProcessingPipeline:
    def __init__(self):
        self.parser = EmailParser()
        self.classifier = KeywordClassifier()
        self.router = Router()
        self.logger = Logger()

        self.stats = defaultdict(int)
        self.base_dir = Path(__file__).resolve().parents[1]

    def process_emails(self):
        inbox = self.base_dir / "inbox"

        if not inbox.exists():
            self.logger.error("Inbox directory не существует")
            return

        if not inbox.is_dir():
            self.logger.error("Inbox path не директория")
            return

        processed = 0
        failed = 0

        for filepath in sorted(inbox.iterdir()):

            if not filepath.is_file():
                continue

            try:
                email = self.parser.parse(str(filepath))
                category, confidence = self.classifier.classify(email)
                is_draft = not email.recipient.strip()

                self.router.route(
                    str(filepath),
                    email.sender,
                    category,
                    is_draft=is_draft
                )
                self.stats[category] += 1
                processed += 1
                self.logger.info(f"{filepath.name} -> {category} " f"(количество совпавших слов = {confidence})")

            except Exception as e:
                failed += 1
                self.stats["errors"] += 1
                self.logger.error(f"{filepath.name}: {str(e)}")

                try:
                    self.router.route(str(filepath),"unknown","errors")
                except Exception:
                    pass

        self.print_statistics(processed, failed)

    def print_statistics(self, processed, failed):
        print("\n=== Итоги ===")
        print(f"Удачные: {processed}")
        print(f"Провалившиеся: {failed}")
        for category, count in sorted(self.stats.items()):
            print(f"{category}: {count}")


if __name__ == "__main__":
    args = parse_arguments()
    if not validate(inbox_dir=args.inbox, config_path=args.config):
        print("Валидация не пройдена. Запуск остановлен.")
        sys.exit(1)
    pipeline = EmailProcessingPipeline()
    pipeline.process_emails()
