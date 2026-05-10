import json
import os

CATALOG_FILE = "data/catalog.json"

def save_catalog(catalog):

    tables = []

    for name, table in (
        catalog.tables.items()
    ):

        tables.append({

            "name": name,

            "schema": table.schema
        })

    with open(
        CATALOG_FILE,
        "w"
    ) as f:

        json.dump(tables, f)

def load_catalog():

    if not os.path.exists(
        CATALOG_FILE
    ):

        return []

    with open(
        CATALOG_FILE,
        "r"
    ) as f:

        return json.load(f)