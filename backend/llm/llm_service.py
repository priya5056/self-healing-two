from llm.gemini_client import client

def generate(prompt):

    MODEL = "gemini-3.1-flash-lite"

    print("MODEL =", MODEL)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text