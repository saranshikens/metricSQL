from storage.catalog import Catalog

class Database:

    def __init__(self):

        self.catalog = Catalog()

        self.initialize()

    def initialize(self):

        if "documents" not in (
            self.catalog.tables
        ):

            self.catalog.create_table(

                "documents",

                {
                    "content": "VECTOR_TEXT"
                }
            )

            table = self.catalog.get_table(
                "documents"
            )

            seed_documents = [

                {
                    "content":
                    "space exploration mission"
                },

                {
                    "content":
                    "deep sea fishing adventure"
                },

                {
                    "content":
                    "astronomy and galaxies"
                },

                {
                    "content":
                    "cooking italian pasta"
                },

                {
                    "content":
                    "rocket launch into orbit"
                },

                {
                    "content":
                    "machine learning systems"
                }
            ]

            for row in seed_documents:

                table.insert(row)