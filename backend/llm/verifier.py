from llm.llm_service import generate
import json


def verify_answer(question, context, answer):

    prompt = f"""
You are an Evidence Verification Agent.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Determine whether EVERY important fact in the answer is supported by the retrieved context.

Return ONLY valid JSON.

Example if supported:

{{
    "supported": true,
    "missing_facts": [],
    "score": 95
}}

Example if unsupported:

{{
    "supported": false,
    "missing_facts": [
        "Faculty experience not found in context"
    ],
    "score": 40
}}
"""

    response = generate(prompt)

    try:
        return json.loads(response)

    except:
        return {
            "supported": False,
            "missing_facts": ["Verification failed"],
            "score": 0
        }