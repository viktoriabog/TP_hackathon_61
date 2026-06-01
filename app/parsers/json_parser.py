import json

from app.models.email import Email


class JsonParser:

    def parse(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return Email(
            subject=data.get("subject", ""),
            body=data.get("body", ""),
            sender=data.get("sender", ""),
            recipient=data.get("recipient", data.get("to", "")),
            filepath=filepath
        )