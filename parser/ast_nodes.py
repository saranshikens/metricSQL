from dataclasses import dataclass

@dataclass
class SelectQuery:

    table: str

    where_column: str | None = None

    where_value: str | None = None

    similar_column: str | None = None

    similar_to: str | None = None

    top_k: int = 1


@dataclass
class InsertQuery:

    table: str

    values: list[str]


@dataclass
class CreateTableQuery:

    table: str

    schema: dict


@dataclass
class DeleteQuery:

    table: str

    where_column: str

    where_value: str