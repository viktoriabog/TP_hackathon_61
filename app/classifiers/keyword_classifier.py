import json
from pathlib import Path


class KeywordClassifier:

    def __init__(self):

        config_path = Path("config/categories.json")

        with open(config_path, "r", encoding="utf-8") as f:
            self.categories = json.load(f)

    def classify(self, email):

        text = (
            email.subject.lower() +
            " " +
            email.body.lower()
        )

        scores = {}

        for category, keywords in self.categories.items():

            score = 0

            for keyword in keywords:

                if keyword.lower() in text:
                    score += 1

            scores[category] = score

        best_category = max(scores, key=scores.get)

        confidence = scores[best_category]

        if confidence == 0:
            return ("unknown", 0)

        return (best_category, confidence)
    

    #АЛЕ