from llm.llm_service import generate
import json


def critic_agent(
    question,
    context,
    answer
):

    # -------------------------
    # No Context
    # -------------------------

    if context.strip() == "":
        return {
            "decision": "NO",
            "confidence": 0
        }

    # -------------------------
    # Generator fallback
    # -------------------------

    if (
        "don't have information" in answer.lower()
        or
        "answer unavailable" in answer.lower()
        or
        "sorry" in answer.lower()
    ):

        return {
            "decision": "NO",
            "confidence": 0
        }

    prompt = f"""
You are a strict RAG evaluator.

Question:

{question}

Context:

{context}

Answer:

{answer}

Rules:

Return YES only if ALL information
in the answer is supported by Context.

If the answer contains even one
unsupported fact,
return NO.

Return ONLY JSON.

Example:

{{
    "decision":"YES",
    "confidence":96
}}

or

{{
    "decision":"NO",
    "confidence":18
}}
"""

    response = generate(prompt)

    try:

        result = json.loads(response)

    except Exception:

        return {
            "decision": "NO",
            "confidence": 0
        }

    return result