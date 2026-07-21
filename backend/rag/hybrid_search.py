from rank_bm25 import BM25Okapi
import numpy as np


def hybrid_search(

    query,

    chunks,

    faiss_indices,

    top_k

):

    corpus = [

        chunk["text"]

        for chunk in chunks

    ]

    tokenized = [

        doc.lower().split()

        for doc in corpus

    ]

    bm25 = BM25Okapi(tokenized)

    scores = bm25.get_scores(

        query.lower().split()

    )

    bm25_indices = np.argsort(scores)[::-1][:top_k * 3]

    merged = []

    seen = set()

    for idx in list(faiss_indices[0]) + list(bm25_indices):

        if idx not in seen:

            seen.add(idx)

            merged.append(chunks[idx])

    return merged[:top_k]