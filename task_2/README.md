# Scraping quotes and importing to MongoDB Atlas

The scraper collects all quotes and their unique authors from
`https://quotes.toscrape.com/` into `qoutes.json` and `authors.json`.

## Run

From `task_2`, install the dependencies and scrape the site:

```bash
python3 -m pip install -r requirements.txt
python3 scrape_quotes.py
```

Set `MONGODB_URI` in `atlas-credentials.env` to the Atlas connection string.
The importer uses the database named in that URI, or `MONGODB_DATABASE` if
provided; if neither specifies a database, it uses `quotes_db`.

Import the files into the `authors` and `qoutes` collections:

```bash
python3 import_to_mongodb.py
```

Imports update documents by author name or quote text, so rerunning the importer
does not add duplicate copies of those records.
