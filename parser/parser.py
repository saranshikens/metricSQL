from lark import Lark

from parser.transformer import SQLTransformer

with open("parser/grammar.lark") as f:
    grammar = f.read()

sql_parser = Lark(
    grammar,
    parser="lalr",
    transformer=SQLTransformer()
)

def parse_query(query: str):

    return sql_parser.parse(query)