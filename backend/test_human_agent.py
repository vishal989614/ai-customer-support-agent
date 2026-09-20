from agents.graph import build_support_graph


agent = build_support_graph()


tests = [
    {
        "question": "I was charged twice for my order. I need human help.",
        "user_id": 4
    },
    {
        "question": "My order has a problem. I want to talk to a human.",
        "user_id": 5
    },
    {
        "question": "My delivery is very late. Please connect me to a human.",
        "user_id": 6
    },
    {
        "question": "I need to speak with a human about something.",
        "user_id": 4
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

    print("\nIssue Type:")
    print(result.get("issue_type"))

    print("\nPriority:")
    print(result.get("priority"))

    print("\nTool Result:")
    print(result.get("tool_result"))

    print("\nVerification:")
    print(result.get("verification_result"))

    print("\nFinal Answer:")
    print(result.get("answer"))