from langgraph.graph import StateGraph, END

from agentic.state import GraphState

from agentic.nodes import (
    planner_node,
    retriever_node,
    generator_node,
    critic_node,
    reflection_node
)

builder = StateGraph(GraphState)


# -----------------------
# Nodes
# -----------------------

builder.add_node("planner", planner_node)
builder.add_node("retriever", retriever_node)
builder.add_node("generator", generator_node)
builder.add_node("critic", critic_node)
builder.add_node("reflection", reflection_node)



# -----------------------
# Entry Point
# -----------------------

builder.set_entry_point("planner")


# -----------------------
# Edges
# -----------------------

def planner_route(state):

    print("Routing Strategy =", state["strategy"])

    if state["strategy"] == "none":
        print("END GRAPH")
        return END

    return "retriever"

builder.add_conditional_edges(
    "planner",
    planner_route
)
builder.add_edge("retriever", "generator")
builder.add_edge("generator", "critic")


# -----------------------
# Conditional Routing
# -----------------------

def route(state):

    # Stop immediately if Reflection decided to stop
    if state["memory"]:

        if state["memory"][-1]["action"] == "stop":
            print("Reflection requested STOP.")
            return END

    # Answer approved
    if state["approved"]:
        return END

    # Maximum retries reached
    if state["retry"] >= 2:
        print("Maximum retries reached.")
        return END

    return "reflection"


builder.add_conditional_edges(

    "critic",

    route

)

builder.add_edge(

    "reflection",

    "planner"

)


graph = builder.compile()