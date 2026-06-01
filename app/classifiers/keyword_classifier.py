from pathlib import Path
import json

class KeywordClassifier:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).resolve().parents[2] / "config" / "categories.json"
        else:
            config_path = Path(config_path)

        with open(config_path, "r", encoding="utf-8") as f:
            self.categories = json.load(f)

    def classify(self, email):

        if not email or not hasattr(email, "subject") or not hasattr(email, "body"):
            return ("unknown", 0)

        subject = (email.subject or "").lower()
        body = (email.body or "").lower()
        text = subject + " " + body

        scores = {}

        for category, keywords in self.categories.items():
            score = 0
            for keyword in keywords:
                if keyword and keyword.lower() in text:
                    score += 1
            scores[category] = score

        if not scores:
            return ("unknown", 0)

        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]

        if confidence == 0:
            return ("unknown", 0)

        return (best_category, confidence)
