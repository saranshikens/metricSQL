from parser.parser import parse_query

from engine.database import Database
from engine.executor import QueryExecutor

db = Database()

executor = QueryExecutor(db)

queries = [

'''
CREATE TABLE papers (
    id INT,
    year TEXT,
    title TEXT,
    abstract VECTOR_TEXT
)
''',

'''
INSERT INTO papers
VALUES (
    "1",
    "2024",
    "Black Hole Thermodynamics",
    "Quantum gravity and event horizons"
)
''',

'''
INSERT INTO papers
VALUES (
    "2",
    "2023",
    "Galaxy Formation",
    "Dark matter cosmology simulations"
)
''',

'''
DELETE FROM papers
WHERE year = "2023"
''',

'''
SELECT * FROM papers
SIMILAR TO abstract "cosmology"
TOP 5
'''
]

for q in queries:

    result = executor.execute(
        parse_query(q)
    )

    print()

    for r in result:

        print(r)