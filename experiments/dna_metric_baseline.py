import time

import Levenshtein

from dna_dataset import dataset

query = dataset[0]

print("\nQuery:\n")

print(query)

start = time.time()

distances = []

for seq in dataset:

    d = Levenshtein.distance(
        query,
        seq
    )

    distances.append((d, seq))

distances.sort(key=lambda x: x[0])

end = time.time()

print(
    f"\nMetric search time: "
    f"{end-start:.6f}s"
)

print("\nTop Matches:\n")

for d, seq in distances[:5]:

    print(
        f"Distance={d}",
        seq
    )