import sys

sys.path.append("similarity/cpp")

from ght_cpp import GHTIndex

from similarity.embeddings import embed_text
from similarity.dataset import documents

class SemanticSearchEngine:

    def __init__(self):

        self.index = GHTIndex(4)

        self.vectors = []

        self.build_index()

    def build_index(self):

        for doc in documents:

            vector = embed_text(doc)

            self.vectors.append(vector)

        self.index.build(self.vectors)

    def search(self, query: str, top_k=1):

        query_vector = embed_text(query)

        indices = self.index.top_k_search(
            query_vector,
            top_k
        )

        return [
            documents[i]
            for i in indices
        ]