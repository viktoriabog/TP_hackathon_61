import argparse
import json
from pathlib import Path

def validate(inbox_dir="inbox", config_path="config/categories.json"):
    errors = []
    warnings = []

    inbox = Path(inbox_dir)
    if not inbox.exists():
        errors.append(f"Папка '{inbox_dir}' не найдена")
    elif not inbox.is_dir():
        errors.append(f"'{inbox_dir}' не является папкой")
    else:
        files = list(inbox.glob("*"))
        if not files:
            warnings.append(f"Папка '{inbox_dir}' пуста")

    config_path = Path(config_path)
    if not config_path.exists():
        errors.append(f"Файл '{config_path}' не найден")
    else:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                categories = json.load(f)
            if not isinstance(categories, dict):
                errors.append("Файл конфига не содержит JSON-объект")
        except json.JSONDecodeError:
            errors.append("Файл конфига содержит невалидный JSON")

    if errors:
        print("Ошибки валидации:")
        for e in errors:
            print(f"   - {e}")
        return False
    else:
        print("Валидация пройдена")
        if warnings:
            print("Предупреждения:")
            for w in warnings:
                print(f"   - {w}")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Проверка окружения")
    parser.add_argument("--inbox", "-i", default="inbox")
    parser.add_argument("--config", "-c", default="config/categories.json")
    args = parser.parse_args()
    success = validate(args.inbox, args.config)
    exit(0 if success else 1)