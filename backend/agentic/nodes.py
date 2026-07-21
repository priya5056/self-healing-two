from agentic.state import GraphState

from llm.planner import planner_agent

from rag.retriever import retrieve_chunks

from llm.generator import generator_agent

from llm.critic import critic_agent

from llm.reflection import reflection_agent

from rag.reranker import rerank

# from llm.verifier import verify_answer

def planner_node(state):

    print(">>> Planner START")
    print("\n===== PLANNER NODE =====")

    plan = planner_agent(
        state["query"],
        state["memory"]
    )

    # -----------------------------
    # Preserve Reflection Strategy
    # -----------------------------
    if state["memory"]:

        last = state["memory"][-1]

        if last["action"] == "change_strategy":

            print("Planner using Reflection Strategy")

            plan["strategy"] = state["strategy"]

    print("PLAN =", plan)

    # -----------------------------
    # Stop immediately
    # -----------------------------
    if plan.get("strategy") == "none":

        state["strategy"] = "none"
        state["approved"] = False
        state["answer"] = (
            "I don't have information about this "
            "in the knowledge base."
        )
        state["sources"] = []
        state["trace"].append("Planner")

        print("Planner decided to stop.")
        print(">>> Planner END")

        return state

    # -----------------------------
    # Update State
    # -----------------------------
    state["keywords"] = plan.get(
        "keywords",
        []
    )

    state["category"] = plan.get(
        "category",
        ""
    )

    state["strategy"] = plan.get(
        "strategy",
        state.get("strategy", "semantic")
    )

    print("========================")
    print("Planner Strategy =", state["strategy"])
    print(">>> Planner END")

    state["trace"].append("Planner")

    return state
    


def retriever_node(state):
    print(">>> Retriever START")
    print("\n===== RETRIEVER =====")

    chunks = retrieve_chunks(

    query=state["query"],

    keywords=state["keywords"],

    category=state["category"],

    strategy=state["strategy"],

    top_k=state["top_k"]

    )

    print(

        f"Retrieved : {len(chunks)}"

    )

    print(

        "Running Cross Encoder..."

    )

    chunks = rerank(
    state["query"],
    chunks
    )

    if len(chunks) == 0:

       print("No relevant chunks found.")

       state["approved"] = False

       state["answer"] = (
        "I don't have information about this in the knowledge base."
       )

       state["sources"] = []

       state["trace"].append("Retriever")

       return state

    context = ""

    sources = []

    for chunk in chunks:

        context += (

            chunk["text"]

            + "\n\n"

        )

        sources.append(

            chunk["source"]

        )

    state["context"] = context

    state["sources"] = list(

        set(sources)

    )

    print(

        "Top Sources :",

        state["sources"]

    )

    print("=================== ==\n")
    print(">>> Retriever END")
    state["trace"].append("Retriever")
    return state

    


def generator_node(state):

    # No context -> directly stop
    if state["context"].strip() == "":

        state["approved"] = False

        state["answer"] = (
            "I don't have information about this "
            "in the knowledge base."
        )

        state["trace"].append("Generator")

        return state

    print(">>> Generator START")

    answer = generator_agent(

        state["query"],

        state["context"]

    )

    state["answer"] = answer

    state["trace"].append("Generator")

    print(">>> Generator END")

    return state

def critic_node(state):

    print(">>> CRITIC START")

    # ---------------------------------
    # Generator already returned fallback
    # ---------------------------------

    if (
        "sorry" in state["answer"].lower()
        or
        "don't have" in state["answer"].lower()
        or
        "unavailable" in state["answer"].lower()
    ):

        print("Fallback answer detected.")

        state["approved"] = False
        state["confidence"] = 0

        state["trace"].append("Critic")

        print(">>> CRITIC END")

        return state

    # ---------------------------------
    # Normal Critic
    # ---------------------------------

    result = critic_agent(

        state["query"],

        state["context"],

        state["answer"]

    )

    print(result)

    state["approved"] = (

        result["decision"] == "YES"

    )

    state["confidence"] = result["confidence"]

    # ---------------------------------
    # Hallucination Detection
    # ---------------------------------

    if state["context"]:

        if "sorry, answer unavailable" in state["answer"].lower():

            print("Hallucination detected.")

            state["approved"] = False
            state["confidence"] = 0

    print(

        "Approved :",

        state["approved"]

    )

    print(

        "Confidence :",

        state["confidence"]

    )
    
    state["trace"].append("Critic")

    print(">>> CRITIC END")

    return state

def reflection_node(state):

    print(">>> Reflection START")
    print("\n===== REFLECTION =====")

    reflection = reflection_agent(
        state["query"],
        state["context"],
        state["answer"]
    )

    print(reflection)

    state["retry"] += 1

    action = reflection.get("action", "stop")

    # -------------------------
    # Apply reflection action
    # -------------------------

    if action == "rewrite_query":

        state["query"] = reflection.get(
            "improved_query",
            state["query"]
        )

    elif action == "increase_top_k":

        state["top_k"] += 3

    elif action == "change_strategy":

        state["strategy"] = reflection.get(
            "strategy",
            "hybrid"
        )

    elif action == "stop":

     state["approved"] = False
     state["strategy"] = "none"

     state["answer"] = (
        "I don't have information about this "
        "in the knowledge base."
     )

     state["memory"].append({

        "attempt": state["retry"],
        "reason": reflection.get(
            "failure_reason",
            ""
        ),
        "action": "stop"

     })

     state["trace"].append("Reflection")

     print(">>> Reflection END")

     return state