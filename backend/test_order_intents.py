from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    {
        "question": "Where is my order?",
        "user_id": 4
    },

    {
        "question": "What is the status of my order?",
        "user_id": 4
    },

    {
        "question": "Show me my order details",
        "user_id": 4
    },


]


for test in tests:

    print("\n")
    print("=" * 60)
    print("QUESTION:", test["question"])
    print("=" * 60)

    result = agent.invoke(
        {
            "question": test["question"],
            "user_id": test["user_id"]
        }
    )

    print("Capability:")
    print(result.get("capability"))

    print("Intent:")
    print(result.get("intent"))

    print("Order ID:")
    print(result.get("order_id"))

    print("Tool Result:")
    print(result.get("tool_result"))

    print("Verification:")
    print(result.get("verification_result"))

    print("Final Answer:")
    print(result.get("answer"))