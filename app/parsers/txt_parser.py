from app.models.email import Email
import re

class TxtParser:

    def parse(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        sender = "unknown"
        subject = ""

        for line in content.splitlines():

            line_lower = line.lower().strip()

            if (
                line_lower.startswith("from:")
                or
                line_lower.startswith("от кого:")
            ):

                sender_text = line.split(":", 1)[1].strip()

                match = re.search(
                    r"<([^>]+)>",
                    sender_text
                )

                if match:
                    sender = match.group(1)
                else:
                    sender = sender_text

            elif (
                line_lower.startswith("subject:")
                or
                line_lower.startswith("тема:")
            ):

                subject = line.split(
                    ":",
                    1
                )[1].strip()

        return Email(
            subject=subject,
            body=content,
            sender=sender,
            filepath=filepath
        )