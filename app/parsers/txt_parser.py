from app.models.email import Email
import re

class TxtParser:

    def parse(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        sender = "unknown"
        subject = ""
        recipient = ""

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
            elif (
                line_lower.startswith("to:")
                or
                line_lower.startswith("komu:")
                or
                line_lower.startswith("кому:")
                or
                line_lower.startswith("poluchatel:")
                or
                line_lower.startswith("получатель:")
                or
                line_lower.startswith("recipient:")
                or
                line_lower.startswith("adresat:")
                or
                line_lower.startswith("адресат:")
            ):

                recipient = line.split(":",1)[1].strip()
            

        return Email(
            subject=subject,
            body=content,
            sender=sender,
            recipient=recipient,
            filepath=filepath
        )