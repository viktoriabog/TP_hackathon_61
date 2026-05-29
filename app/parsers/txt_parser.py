from app.models.email import Email


class TxtParser:

    def parse(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        return Email(
            subject="TXT Email",
            body=content,
            sender="unknown",
            filepath=filepath
        )