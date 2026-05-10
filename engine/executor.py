from parser.ast_nodes import (

    SelectQuery,

    InsertQuery,

    CreateTableQuery,

    DeleteQuery
)

class QueryExecutor:

    def __init__(self, database):

        self.database = database

    def execute(self, query_ast):

        if isinstance(query_ast, SelectQuery):

            return self.execute_select(
                query_ast
            )

        if isinstance(query_ast, InsertQuery):

            return self.execute_insert(
                query_ast
            )

        if isinstance(query_ast, CreateTableQuery):

            return self.execute_create_table(
                query_ast
            )

        if isinstance(query_ast, DeleteQuery):

            return self.execute_delete(
                query_ast
            )

        raise ValueError(
            "Unknown query type"
        )

    def execute_select(self, query):

        table = (
            self.database
            .catalog
            .get_table(query.table)
        )

        candidate_rows = table.rows

        if query.where_column:

            candidate_rows = (
                table.filter_rows(
                    query.where_column,
                    query.where_value
                )
            )

        results = table.semantic_search(

            query.similar_column,

            query.similar_to,

            query.top_k,

            candidate_rows
        )

        return results

    def execute_insert(self, query):

        table = (
            self.database
            .catalog
            .get_table(query.table)
        )

        columns = list(
            table.schema.keys()
        )

        values = {}

        for col, val in zip(
            columns,
            query.values
        ):

            values[col] = val

        table.insert(values)

        return [
            f"Inserted into {query.table}"
        ]

    def execute_create_table(self, query):

        self.database.catalog.create_table(

            query.table,

            query.schema
        )

        return [
            f"Table created: {query.table}"
        ]

    def execute_delete(self, query):

        table = (
            self.database
            .catalog
            .get_table(query.table)
        )

        deleted_count = table.delete_rows(

            query.where_column,

            query.where_value
        )

        return [

            f"Deleted {deleted_count} rows"
        ]