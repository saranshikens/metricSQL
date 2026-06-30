import time

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from dna_dataset import dataset

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("\nGenerating embeddings...\n")

start = time.time()

embeddings = model.encode(dataset)

end = time.time()

print(
    f"Embedding generation time: "
    f"{end-start:.2f}s"
)

query = dataset[0]

print("\nQuery:\n")

print(query)

query_embedding = model.encode([query])

start = time.time()

scores = cosine_similarity(
    query_embedding,
    embeddings
)[0]

top_indices = scores.argsort()[-5:][::-1]

end = time.time()

print(
    f"\nSearch time: "
    f"{end-start:.6f}s"
)

print("\nTop Matches:\n")

for idx in top_indices:

    print(dataset[idx])