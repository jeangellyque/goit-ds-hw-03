from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import unquote, urlparse

from dotenv import dotenv_values
from pymongo import MongoClient, UpdateOne


TASK_DIR = Path(__file__).resolve().parent
ENV_FILE = TASK_DIR / "atlas-credentials.env"


def load_json(filename: str) -> list[dict[str, object]]:
    data = json.loads((TASK_DIR / filename).read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"{filename} must contain a non-empty JSON array")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"{filename} must contain only JSON objects")
    return data


def main() -> None:
    settings = dotenv_values(ENV_FILE)
    uri = settings.get("MONGODB_URI")
    if not uri:
        raise ValueError(f"MONGODB_URI is missing from {ENV_FILE}")

    parsed_uri = urlparse(uri)
    database_name = settings.get("MONGODB_DATABASE") or unquote(
        parsed_uri.path.lstrip("/").split("/", 1)[0]
    )
    database_name = database_name or "quotes_db"

    authors = load_json("authors.json")
    quotes = load_json("qoutes.json")

    with MongoClient(uri, serverSelectionTimeoutMS=15000) as client:
        client.admin.command("ping")
        database = client[database_name]

        for collection_name in ("authors", "qoutes"):
            if collection_name not in database.list_collection_names():
                database.create_collection(collection_name)

        author_operations = [
            UpdateOne(
                {"fullname": author["fullname"]},
                {"$set": author},
                upsert=True,
            )
            for author in authors
        ]
        quote_operations = [
            UpdateOne(
                {"quote": quote["quote"]},
                {"$set": quote},
                upsert=True,
            )
            for quote in quotes
        ]

        database["authors"].bulk_write(author_operations)
        database["qoutes"].bulk_write(quote_operations)

        print(
            f"Imported into {database_name}: "
            f"{database['authors'].count_documents({})} authors, "
            f"{database['qoutes'].count_documents({})} quotes."
        )


if __name__ == "__main__":
    main()
