from dataclasses import dataclass

@dataclass
class Row:

    id: int

    values: dict

    embeddings: dict

    deleted: bool = False