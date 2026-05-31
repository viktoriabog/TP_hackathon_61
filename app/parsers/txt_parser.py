import re
from app.models.email import Email
class TxtParser:

    def parse(self, filepath):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        sender = "unknown"

        match = re.search(
            r"From:.*<(.+?)>",
            content
        )

        if match:
            sender = match.group(1)

        subject = ""

        match = re.search(
            r"Subject:(.+)",
            content
        )

        if match:
            subject = match.group(1).strip()

        return Email(
            subject=subject,
            body=content,
            sender=sender,
            filepath=filepath
        )