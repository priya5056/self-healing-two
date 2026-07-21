from typing import TypedDict


class GraphState(TypedDict):

    query: str

    context: str

    answer: str

    keywords: list

    category: str

    sources: list

    verification_score: int

    supported: bool

    retry: int

    approved: bool

    confidence: int

    trace: list

    strategy: str

    top_k: int

    memory: list