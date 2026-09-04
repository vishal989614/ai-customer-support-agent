from langgraph.graph import (
    StateGraph,
    START,
    END
)

from .state import SupportState

from .nodes import (
    understand_request,
    rag_node,
    order_node,
    payment_node,
    restaurant_node,
    delivery_node,
    human_node,
    verify_node,
    generate_response
)

from .router import capability_router

def build_support_graph():

    graph = StateGraph(
        SupportState
    )

    # Add nodes

    graph.add_node(
        "understand_request",
        understand_request
    )

    graph.add_node(
        "rag",
        rag_node
    )

    graph.add_node(
        "order",
        order_node
    )

    graph.add_node(
        "payment",
        payment_node
    )

    graph.add_node(
        "restaurant",
        restaurant_node
    )

    graph.add_node(
        "delivery",
        delivery_node
    )

    graph.add_node(
        "human",
        human_node
    )

    graph.add_node(
        "verify",
        verify_node
    )

    graph.add_node(
        "generate_response",
        generate_response
    )

    # START → Understand Request

    graph.add_edge(
        START,
        "understand_request"
    )

     # Select capability

    graph.add_conditional_edges(
        "understand_request",
        capability_router,
        {
            "rag": "rag",
            "order": "order",
            "payment": "payment",
            "restaurant": "restaurant",
            "delivery": "delivery",
            "human": "human"
        }
    )

    # Execute → Verify

    graph.add_edge("rag", "verify")
    graph.add_edge("order", "verify")
    graph.add_edge("payment", "verify")
    graph.add_edge("restaurant", "verify")
    graph.add_edge("delivery", "verify")
    graph.add_edge("human", "verify")

     # Verify → Generate Response

    graph.add_edge(
        "verify",
        "generate_response"
    )

    # Generate Response → END

    graph.add_edge(
        "generate_response",
        END
    )

    return graph.compile()