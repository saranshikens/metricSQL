from storage.table import Table

from storage.catalog_serializer import (
    save_catalog,
    load_catalog
)

class Catalog:

    def __init__(self):

        self.tables = {}

        self.load_existing_tables()

    def load_existing_tables(self):

        catalog_data = load_catalog()

        for entry in catalog_data:

            name = entry["name"]

            schema = entry["schema"]

            self.tables[name] = Table(
                name,
                schema
            )

    def create_table(
        self,
        name,
        schema
    ):

        if name not in self.tables:

            self.tables[name] = Table(
                name,
                schema
            )

            save_catalog(self)

    def get_table(self, name):

        if name not in self.tables:

            raise ValueError(
                f"Table '{name}' does not exist"
            )

        return self.tables[name]