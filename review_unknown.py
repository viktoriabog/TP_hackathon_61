import json
import shutil
from pathlib import Path

from app.classifiers.keyword_classifier import KeywordClassifier


OUTPUT_DIR = Path("output")
CONFIG_PATH = Path("config/categories.json")


def load_categories():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_categories(categories):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)


def extract_keywords(text: str):
    words = text.lower().split()
    return [
        w.strip(".,!?()[]{}:;\"'")
        for w in words
        if len(w.strip(".,!?()[]{}:;\"'")) > 3
    ]


def move_file(file_path: Path, category: str):
    target_dir = OUTPUT_DIR / category
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / file_path.name
    shutil.move(str(file_path), str(target_path))

def is_low_quality(text: str) -> bool:
    words = text.strip().split()

    if len(words) < 3:
        return True

    meaningful = [w for w in words if len(w) > 3]

    return len(meaningful) < 2

def retrain_unknown():
    classifier = KeywordClassifier()
    unknown_dir = OUTPUT_DIR / "unknown"

    for file in list(unknown_dir.glob("*")):
        if not file.is_file():
            continue

        text = file.read_text(encoding="utf-8", errors="ignore").strip()

        if not text:
            move_file(file, "empty")
            print(f"empty: {file.name}")
            continue

        if is_low_quality(text):
            move_file(file, "low_quality")
            print(f"low_quality: {file.name}")
            continue
        email = type("Email", (), {
            "subject": "",
            "body": text
        })

        category, confidence = classifier.classify(email)
        if category == "unknown":
            continue
        if confidence < 2:
            continue

        move_file(file, category)
        print(f"auto: {file.name} -> {category} ({confidence})")


def review():
    categories = load_categories()
    unknown_dir = OUTPUT_DIR / "unknown"

    if not unknown_dir.exists():
        print("Нет папки output/unknown")
        return

    while True:
        files = list(unknown_dir.glob("*"))

        if not files:
            print("\nНет неизвестных писем")
            break

        file = files[0]

        print("\n" + "=" * 60)
        print(f"Письмо: {file.name}")

        text = file.read_text(encoding="utf-8", errors="ignore").strip()

        if not text:
            move_file(file, "empty")
            print("Пустое письмо -> empty")
            continue

        print("Содержимое:\n")
        print(text[:400])

        available = list(categories.keys())

        if not available:
            print("Нет категорий в системе")
            return

        print("\nВыберите категорию:")
        for i, cat in enumerate(available, 1):
            print(f"{i}. {cat}")

        print(f"{len(available) + 1}. пропустить")

        try:
            choice = int(input("Ваш выбор: "))
        except ValueError:
            print("Некорректный ввод")
            continue

        if choice == len(available) + 1:
            print("⏭ пропущено")
            move_file(file, "unknown_skipped")
            continue

        if choice < 1 or choice > len(available):
            print("Неверный выбор")
            continue

        category = available[choice - 1]
        move_file(file, category)
        keywords = extract_keywords(text)

        if not keywords:
            keywords = ["__empty__"]

        existing = set(categories.get(category, []))
        existing.update(keywords)
        categories[category] = list(existing)

        save_categories(categories)

        print(f"Обучено: {category}")
        print(f"слов добавлено: {len(keywords)}")
        retrain_unknown()

    print("\nОбучение завершено полностью")

if __name__ == "__main__":
    review()
