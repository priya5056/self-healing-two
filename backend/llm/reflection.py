from llm.llm_service import generate
import json


def reflection_agent(

    question,

    context,

    answer

):

    prompt = f"""
You are the Reflection Agent of a Self-Healing RAG.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Find the failure reason.

Then decide ONE next action.

Available actions:

1. rewrite_query
2. increase_top_k
3.change_strategy
4.stop

Available retrieval strategies:

semantic

hybrid

metadata

Return ONLY JSON.

Example:

{{
    "failure_reason":"Too few chunks",

    "action":"increase_top_k",

    "improved_query":"",

    "strategy":"semantic",

    "retry":true
}}

Example:

{{
    "failure_reason":"Wrong retrieval",

    "action":"change_strategy",

    "strategy":"hybrid",

    "retry":true
}}

Example:

{{
    "failure_reason":"Query too broad",

    "action":"rewrite_query",

    "improved_query":"Who teaches Biology?",

    "strategy":"semantic",

    "retry":true
}}

Example:

{{
    "failure_reason":"No related documents",

    "action":"stop",

    "retry":false
}}
"""

    response = generate(prompt)

    try:

        return json.loads(response)

    except:

        return {

            "failure_reason":"Unknown",

            "action":"stop",

            "retry":False

        }