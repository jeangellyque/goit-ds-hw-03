from __future__ import annotations

import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "cats_db"
COLLECTION_NAME = "cats"


def get_collection() -> Collection:
    """Create MongoDB connection and return cats collection."""
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


def create_cat(collection: Collection, name: str, age: int, features: list[str]) -> None:
    """Create a new cat document."""
    cat = {"name": name, "age": age, "features": features}
    result = collection.insert_one(cat)
    print(f"Кота додано. _id: {result.inserted_id}")


def show_all_cats(collection: Collection) -> None:
    """Print all cat documents from collection."""
    cats = list(collection.find())
    if not cats:
        print("Колекція порожня.")
        return

    for cat in cats:
        print(cat)


def show_cat_by_name(collection: Collection, name: str) -> None:
    """Print one cat document by name."""
    cat = collection.find_one({"name": name})
    if cat is None:
        print(f"Кота з іменем '{name}' не знайдено.")
        return

    print(cat)


def update_cat_age(collection: Collection, name: str, new_age: int) -> None:
    """Update cat age by name."""
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count == 0:
        print(f"Кота з іменем '{name}' не знайдено.")
        return

    print("Вік кота оновлено.")


def add_cat_feature(collection: Collection, name: str, feature: str) -> None:
    """Add a new feature to cat features list by name."""
    result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.matched_count == 0:
        print(f"Кота з іменем '{name}' не знайдено.")
        return

    print("Характеристику додано.")


def delete_cat_by_name(collection: Collection, name: str) -> None:
    """Delete one cat document by name."""
    result = collection.delete_one({"name": name})
    if result.deleted_count == 0:
        print(f"Кота з іменем '{name}' не знайдено.")
        return

    print("Запис видалено.")


def delete_all_cats(collection: Collection) -> None:
    """Delete all cat documents from collection."""
    result = collection.delete_many({})
    print(f"Видалено записів: {result.deleted_count}")


def print_menu() -> None:
    print(
        "\nОберіть дію:\n"
        "1 - Додати кота\n"
        "2 - Показати всіх котів\n"
        "3 - Знайти кота за ім'ям\n"
        "4 - Оновити вік кота\n"
        "5 - Додати характеристику коту\n"
        "6 - Видалити кота за ім'ям\n"
        "7 - Видалити всі записи\n"
        "0 - Вийти\n"
    )


def read_int(prompt: str) -> int:
    """Read integer value from input with validation."""
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Введіть ціле число.")


def read_features() -> list[str]:
    """Read features from comma-separated user input."""
    raw = input("Введіть характеристики через кому: ").strip()
    return [item.strip() for item in raw.split(",") if item.strip()]


def handle_action(collection: Collection, action: str) -> bool:
    """Handle menu action. Returns False when user exits."""
    if action == "1":
        name = input("Ім'я кота: ").strip()
        age = read_int("Вік кота: ")
        features = read_features()
        create_cat(collection, name, age, features)
    elif action == "2":
        show_all_cats(collection)
    elif action == "3":
        name = input("Введіть ім'я кота: ").strip()
        show_cat_by_name(collection, name)
    elif action == "4":
        name = input("Введіть ім'я кота: ").strip()
        new_age = read_int("Новий вік: ")
        update_cat_age(collection, name, new_age)
    elif action == "5":
        name = input("Введіть ім'я кота: ").strip()
        feature = input("Нова характеристика: ").strip()
        add_cat_feature(collection, name, feature)
    elif action == "6":
        name = input("Введіть ім'я кота: ").strip()
        delete_cat_by_name(collection, name)
    elif action == "7":
        delete_all_cats(collection)
    elif action == "0":
        return False
    else:
        print("Невідома команда.")

    return True


def main() -> None:
    try:
        collection = get_collection()
    except PyMongoError as error:
        print(f"Помилка підключення до MongoDB: {error}")
        return

    while True:
        print_menu()
        action = input("Ваш вибір: ").strip()

        try:
            should_continue = handle_action(collection, action)
        except PyMongoError as error:
            print(f"Помилка MongoDB: {error}")
            continue
        except Exception as error:
            print(f"Непередбачена помилка: {error}")
            continue

        if not should_continue:
            print("Роботу завершено.")
            break


if __name__ == "__main__":
    main()
