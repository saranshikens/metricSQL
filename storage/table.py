from storage.row import Row

from similarity.embeddings import embed_text

from storage.serializer import (
    save_table,
    load_table
)

import sys

sys.path.append("similarity/cpp")

from ght_cpp import GHTIndex

class Table:

    def __init__(
        self,
        name,
        schema=None
    ):

        self.name = name

        self.schema = schema or {}

        self.rows = []

        self.indexes = {}

        self.indexed_rows = []

        self.pending_rows = []

        self.initialize_indexes()

        load_table(self)

    def initialize_indexes(self):

        self.indexes = {}

        for column, col_type in (
            self.schema.items()
        ):

            if col_type == "VECTOR_TEXT":

                self.indexes[column] = (
                    GHTIndex(4)
                )

    def rebuild_indexes(self):

        for column in self.indexes:

            vectors = []

            for row in self.indexed_rows:

                vectors.append(
                    row.embeddings[column]
                )

            if vectors:

                self.indexes[column].build(
                    vectors
                )

    def insert(self, values):

        embeddings = {}

        for column in self.indexes:

            text = values[column]

            embeddings[column] = (
                embed_text(text)
            )

        row = Row(

            id=len(self.rows),

            values=values,

            embeddings=embeddings
        )

        self.rows.append(row)

        self.pending_rows.append(row)

        if len(self.pending_rows) >= 5:

            print(
                f"[INFO] Flushing "
                f"{len(self.pending_rows)} rows "
                f"into GHT index..."
            )

            self.flush_pending_rows()

        save_table(self)

    def flush_pending_rows(self):

        if not self.pending_rows:
            return

        self.indexed_rows.extend(
            self.pending_rows
        )

        self.rebuild_indexes()

        self.pending_rows.clear()

    def semantic_search(
        self,
        column,
        query,
        top_k=1,
        candidate_rows=None
    ):

        if column not in self.indexes:

            raise ValueError(
                f"Column '{column}' "
                f"is not semantic-searchable"
            )

        if not self.rows:
            return []

        query_vector = embed_text(query)

        scored = []


        if self.indexed_rows:

            indices = (
                self.indexes[column]
                .top_k_search(
                    query_vector,
                    top_k
                )
            )

            for idx in indices:

                row = self.get_row_by_id(idx)

                if row is None:
                    continue

                vector = row.embeddings[column]

                distance = sum(

                    (a - b) ** 2

                    for a, b in zip(
                        query_vector,
                        vector
                    )
                )

                scored.append(
                    (distance, row.values)
                )


        for row in self.pending_rows:

            if row.deleted:
                continue

            vector = row.embeddings[column]

            distance = sum(

                (a - b) ** 2

                for a, b in zip(
                    query_vector,
                    vector
                )
            )

            scored.append(
                (distance, row.values)
            )


        if candidate_rows is not None:

            allowed = {

                id(row)

                for row in candidate_rows
            }

            scored = [

                (dist, values)

                for dist, values in scored

                if any(

                    row.values == values

                    and id(row) in allowed

                    for row in candidate_rows
                )
            ]

        scored.sort(key=lambda x: x[0])

        return [

            row

            for _, row in scored[:top_k]
        ]

    def filter_rows(
        self,
        column,
        value
    ):

        return [

            row

            for row in self.rows

            if (
                not row.deleted
                and row.values[column] == value
            )
        ]

    def get_row_by_id(self, row_id):

        for row in self.indexed_rows:

            if row.deleted:
                continue

            if row.id == row_id:

                return row

        return None

    def delete_rows(
        self,
        column,
        value
    ):

        deleted_count = 0

        for row in self.rows:

            if row.deleted:
                continue

            if row.values[column] == value:

                row.deleted = True

                deleted_count += 1

        save_table(self)

        return deleted_count