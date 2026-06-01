import json
import shutil
from pathlib import Path


OUTPUT_DIR = Path("output")

def get_unknown_dir():
    return OUTPUT_DIR / "unknown"
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
    return [w.strip(".,!?()[]{}:;\"'") for w in words if len(w) > 3]


def move_file(file_path: Path, category: str):
    target_dir = OUTPUT_DIR / category
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(target_dir / file_path.name))


def review():
    categories = load_categories()

    if not get_unknown_dir().exists():
        print("Нет папки output/unknown")
        return

    files = list(get_unknown_dir().glob("*"))

    if not files:
        print("Нет неизвестных писем")
        return

    for file in files:
        print("\n" + "=" * 60)
        print(f"Письмо: {file.name}")

        text = file.read_text(encoding="utf-8", errors="ignore")
        print("Содержимое:")
        print(text[:300])

        print("\nВыберите категорию:")
        available = list(categories.keys())

        for i, cat in enumerate(available, 1):
            print(f"{i}. {cat}")
        print(f"{len(available)+1}. пропустить")

        try:
            choice = int(input("Ваш выбор: "))
        except ValueError:
            print("Некорректный ввод, пропуск...")
            continue

        if choice == len(available) + 1:
            continue

        if choice < 1 or choice > len(available):
            print("Неверный выбор")
            continue

        category = available[choice - 1]

        move_file(file, category)

        keywords = extract_keywords(text)
        existing = set(categories.get(category, []))
        existing.update(keywords)
        categories[category] = list(existing)

        print(f"Перемещено в {category}")
        print(f"Добавлено слов: {len(keywords)}")

    save_categories(categories)
    print("\nГотово! Категории обновлены.")


if __name__ == "__main__":
    review()