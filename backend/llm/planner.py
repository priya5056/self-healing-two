from llm.llm_service import generate
import json


def planner_agent(query, memory):

    prompt = f"""
You are a Query Planning Agent.

Your job is to decide the best retrieval strategy.

Knowledge Base Topics:
- Admissions
- Fees
- Faculty
- Batch Timings
- Academic Calendar
- Study Guides
- FAQ

Previous Attempts:
{memory}

IMPORTANT RULES:

1. If memory contains:
   action = "change_strategy"
   then DO NOT use semantic again.
   Choose hybrid.

2. If memory contains:
   action = "stop"
   then return

{{
    "intent":"unknown",
    "category":"",
    "keywords":[],
    "strategy":"none"
}}

3. If the question is clearly outside the coaching knowledge base,
like politics, cricket, weather, movies, celebrities, etc.,
return strategy = "none".

Return ONLY valid JSON.

Example:

{{
    "intent":"faculty_information",
    "category":"Faculty",
    "keywords":["biology","faculty"],
    "strategy":"semantic"
}}

User Query:

{query}
"""

    response = generate(prompt)

    try:

        return json.loads(response)

    except:

        return {

            "intent": "general",

            "category": "",

            "keywords": [query],

            "strategy": "semantic"

        }