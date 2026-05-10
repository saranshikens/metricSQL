import json
import os

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

def table_path(table_name):

    return f"{DATA_DIR}/{table_name}.json"

def save_table(table):

    data = {

        "schema": table.schema,

        "rows": []
    }

    for row in table.rows:

        data["rows"].append({

            "id": row.id,

            "values": row.values,

            "embeddings": row.embeddings,

            "deleted": row.deleted
        })

    with open(
        table_path(table.name),
        "w"
    ) as f:

        json.dump(data, f)

def load_table(table):

    path = table_path(table.name)

    if not os.path.exists(path):
        return

    with open(path, "r") as f:

        data = json.load(f)

    table.schema = data["schema"]

    table.initialize_indexes()

    table.rows.clear()

    from storage.row import Row

    for item in data["rows"]:

        row = Row(

            id=item["id"],

            values=item["values"],

            embeddings=item["embeddings"],

            deleted=item.get(
                "deleted",
                False
            )
        )

        table.rows.append(row)
        table.indexed_rows.append(row)

    table.rebuild_indexes()