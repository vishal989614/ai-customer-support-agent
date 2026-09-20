from agents.graph import build_support_graph


agent = build_support_graph()


tests = [
    {
        "question": "Refund my payment for order 2",
        "user_id": 4
    },
    {
        "question": "Refund my payment for order 3",
        "user_id": 5
    },
    {
        "question": "Refund my payment for order 4",
        "user_id": 6
    }
]


for test in tests:

    print("\n")
    print("=" * 70)
    print("QUESTION:", test["question"])
    print("USER ID:", test["user_id"])
    print("=" * 70)

    result = agent.invoke(
        {
            "question": test["question"],
            "user_id": test["user_id"]
        }
    )

    print("\nCapability:")
    print(result.get("capability"))

    print("\nIntent:")
    print(result.get("intent"))

    print("\nOrder ID:")
    print(result.get("order_id"))

    print("\nTool Result:")
    print(result.get("tool_result"))

    print("\nVerification:")
    print(result.get("verification_result"))

    print("\nFinal Answer:")
    print(result.get("answer"))