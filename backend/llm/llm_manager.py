from llm.gemini_client import client

from core.prompts import system_prompt

from rag.retriever import retrieve_chunks

from llm.critic import critic_agent
from llm.generator import generator_agent


def llm_response(query, conversation=None):

    MAX_RETRIES = 2

    current_query = query

    for attempt in range(MAX_RETRIES + 1):

        print(
            f"\n========== Attempt {attempt + 1} ==========\n"
        )

        similar_chunks = retrieve_chunks(
            current_query
        )

        context = ""

        sources = []

        for chunk in similar_chunks:

            if isinstance(chunk, dict):

                context += (
                    chunk["text"]
                    + "\n\n"
                )

                sources.append(
                    chunk["source"]
                )

            else:

                context += (
                    str(chunk)
                    + "\n\n"
                )

        sources = list(
            set(sources)
        )

        print(
            "\n===== RETRIEVED CONTEXT ====="
        )

        print(context)

        print(
            "=============================\n"
        )

        prompt = (

            system_prompt

            + "\n\nContext:\n"

            + context

            + "\n\nUser Question:\n"

            + current_query

        )

        answer = generator_agent(

            current_query,

            context

        )

        decision = critic_agent(

            question=current_query,

            context=context,

            answer=answer

        )

        print(
            "\n===== CRITIC ====="
        )

        print(decision)

        print(
            "==================\n"
        )
        # ---------------------------------
        # If Critic approves
        # ---------------------------------

        if decision.startswith("YES"):

            if sources:

                answer += "\n\n📄 Sources:\n"

                for source in sources:

                    answer += f"\n• {source}"

            return answer

        # ---------------------------------
        # Critic suggested a better query
        # ---------------------------------

        print("\n===== SELF HEALING =====")

        new_query = current_query

        lines = decision.splitlines()

        for line in lines:

            if line.strip().startswith("Suggested Query:"):

                new_query = (
                    line.replace(
                        "Suggested Query:",
                        ""
                    ).strip()
                )

                break

        print("Old Query :", current_query)

        print("New Query :", new_query)

        print("========================\n")

        # If no better query found,
        # stop retrying

        if (
            new_query == ""
            or
            new_query == current_query
        ):

            break

        current_query = new_query

    # ---------------------------------
    # Fallback
    # ---------------------------------

    return (
        "Sorry, I couldn't find enough information "
        "in the uploaded academic documents "
        "to answer your question accurately."
    )
