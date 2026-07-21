from llm.llm_service import generate
from core.prompts import system_prompt


def generator_agent(query, context):

    if context.strip() == "":
        return "I don't have information about this in the knowledge base."

    prompt = f"""
{system_prompt}

You MUST answer ONLY using the supplied context.

Rules:

1. If the answer exists in the context,
   answer normally.

2. If the answer is NOT present in the context,
   reply EXACTLY:

I don't have information about this in the knowledge base.

3. Never use outside knowledge.

4. Never guess.

5. Never hallucinate.

Context:
{context}

User Question:
{query}
"""

    return generate(prompt)