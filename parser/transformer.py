from lark import Transformer

from parser.ast_nodes import (
    SelectQuery,
    InsertQuery,
    CreateTableQuery,
    DeleteQuery
)

class SQLTransformer(Transformer):

    def start(self, items):
        return items[0]

    def statement(self, items):
        return items[0]

    def select_stmt(self, items):

        table = str(items[0])

        where_column = None

        where_value = None

        similar_column = None

        similar_to = None

        top_k = 1

        for item in items[1:]:

            if isinstance(item, tuple):

                if item[0] == "WHERE":

                    where_column = item[1]

                    where_value = item[2]

                elif item[0] == "SIMILAR":

                    similar_column = item[1]

                    similar_to = item[2]

                elif item[0] == "TOP":

                    top_k = item[1]

        return SelectQuery(

            table=table,

            where_column=where_column,

            where_value=where_value,

            similar_column=similar_column,

            similar_to=similar_to,

            top_k=top_k
        )

    def insert_stmt(self, items):

        table = str(items[0])

        values = items[1]

        return InsertQuery(
            table=table,
            values=values
        )

    def create_table_stmt(self, items):

        table = str(items[0])

        schema = items[1]

        return CreateTableQuery(
            table=table,
            schema=schema
        )

    def similarity_clause(self, items):

        column = str(items[0])

        text = items[1][1:-1]

        return (
            "SIMILAR",
            column,
            text
        )

    def top_clause(self, items):

        return (
            "TOP",
            int(items[0])
        )

    def value_list(self, items):

        return [
            item[1:-1]
            for item in items
        ]

    def column_definitions(self, items):

        schema = {}

        for col_name, col_type in items:

            schema[col_name] = col_type

        return schema

    def column_definition(self, items):

        return (
            str(items[0]),
            str(items[1])
        )

    def where_clause(self, items):

        column = str(items[0])

        value = items[1][1:-1]

        return (
            "WHERE",
            column,
            value
        )

    def delete_stmt(self, items):

        table = str(items[0])

        where_data = items[1]

        return DeleteQuery(

            table=table,

            where_column=where_data[1],

            where_value=where_data[2]
        )