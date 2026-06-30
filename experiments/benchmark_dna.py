import sys
import time

sys.path.append(
    "similarity/cpp"
)

from metric_ght_cpp import MetricGHT

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import Levenshtein

from dna_dataset import dataset

TOP_K = 5

query = dataset[0]

print("\nQUERY:\n")
print(query)

print("\n========================")
print("EMBEDDING BASELINE")
print("========================\n")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

start = time.time()

embeddings = model.encode(dataset)

query_embedding = model.encode(
    [query]
)

scores = cosine_similarity(
    query_embedding,
    embeddings
)[0]

top_indices = (
    scores.argsort()[-TOP_K:][::-1]
)

embedding_time = (
    time.time() - start
)

print(
    f"Search Time: "
    f"{embedding_time:.6f}s"
)

embedding_results = []

print("\nTop Matches:\n")

for idx in top_indices:

    seq = dataset[idx]

    embedding_results.append(idx)

    dist = Levenshtein.distance(
        query,
        seq
    )

    print(
        f"EditDist={dist}",
        seq
    )

print("\n========================")
print("EXACT METRIC SEARCH")
print("========================\n")

start = time.time()

distances = []

for i, seq in enumerate(dataset):

    d = Levenshtein.distance(
        query,
        seq
    )

    distances.append((d, i))

distances.sort()

metric_time = (
    time.time() - start
)

metric_results = [

    idx

    for _, idx

    in distances[:TOP_K]
]

print(
    f"Search Time: "
    f"{metric_time:.6f}s"
)

print("\nTop Matches:\n")

for d, idx in distances[:TOP_K]:

    print(
        f"EditDist={d}",
        dataset[idx]
    )

print("\n========================")
print("GHT METRIC SEARCH")
print("========================\n")

index = MetricGHT(4)

build_start = time.time()

index.build(dataset)

build_time = (
    time.time() - build_start
)

search_start = time.time()

ght_results = index.top_k_search(
    query,
    TOP_K
)

ght_time = (
    time.time() - search_start
)

print(
    f"Build Time: "
    f"{build_time:.6f}s"
)

print(
    f"Search Time: "
    f"{ght_time:.6f}s"
)

print("\nTop Matches:\n")

for idx in ght_results:

    seq = dataset[idx]

    dist = Levenshtein.distance(
        query,
        seq
    )

    print(
        f"EditDist={dist}",
        seq
    )

ground_truth = set(metric_results)

embedding_recall = len(
    ground_truth &
    set(embedding_results)
) / TOP_K

ght_recall = len(
    ground_truth &
    set(ght_results)
) / TOP_K

print("\n========================")
print("RECALL@5")
print("========================\n")

print(
    f"Embedding Recall@5: "
    f"{embedding_recall:.2f}"
)

print(
    f"GHT Recall@5: "
    f"{ght_recall:.2f}"
)