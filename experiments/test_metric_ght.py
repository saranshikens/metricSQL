import sys

sys.path.append(
    "similarity/cpp"
)

from metric_ght_cpp import MetricGHT

from dna_dataset import dataset

index = MetricGHT(4)

index.build(dataset)

query = dataset[0]

print("\nQuery:\n")

print(query)

results = index.top_k_search(
    query,
    5
)

print("\nTop Matches:\n")

for idx in results:

    print(dataset[idx])