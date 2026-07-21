print("FILE =", __file__)

from fastapi import APIRouter
from schemas.chat_schema import ChatRequest
from agentic.workflow import graph
import traceback

router = APIRouter()


@router.post("/chat")
def logic(request: ChatRequest):

    print("\n==============================")
    print("FUNCTION STARTED")
    print("==============================")

    state = {

        "query": request.message,

        "keywords": [],

        "category": "",

        "strategy": "semantic",

        "context": "",

        "sources": [],

        "answer": "",

        "retry": 0,

        "approved": False,

        "confidence": 0,

        "trace": [],

        "top_k": 4,

        "memory": []

    }

    print("\nInitial State")
    print(state)

    try:

        print("\n===== Before graph =====")

        result = graph.invoke(state)
        
        print("\n===== After graph =====")
        print(result)

        print("\n===== Trace =====")
        print(result.get("trace"))

        sources = result.get("sources", [])

        if not result.get("approved", False):
          sources = []
        reply = result.get("answer", "")

        if not reply.strip():
           reply = "I don't have information about this in the knowledge base."
        return {

         "reply": result.get("answer", ""),

         "sources": sources,

          "approved": result.get("approved", False),

         "trace": result.get("trace", [])
 
        }

    except Exception as e:

        print("\n========== GRAPH ERROR ==========")

        traceback.print_exc()

        print("\nException Type :", type(e).__name__)
        print("Exception :", str(e))

        print("\n===============================\n")

        return {

            "reply": "Graph Failed",

            "error": str(e)

        }