from sentence_transformers import CrossEncoder

_model = None


def get_reranker():

    global _model

    if _model is None:

        _model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return _model


def rerank(query, chunks):

    if len(chunks) == 0:

        return []

    model = get_reranker()

    pairs = [

        (
            query,
            chunk["text"]
        )

        for chunk in chunks

    ]

    scores = model.predict(pairs)

    ranked = sorted(

        zip(scores, chunks),

        key=lambda x: x[0],

        reverse=True

    )

    return [

        chunk

        for score, chunk in ranked

    ]