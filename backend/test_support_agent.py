from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    {
        "question": "Mark support ticket 7 as resolved.",
        "user_id": 4
    },
    {
        "question": "What is the status of support ticket 7?",
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

    print("\nTicket ID:")
    print(result.get("ticket_id"))

    print("\nTool Result:")
    print(result.get("tool_result"))

    print("\nVerification:")
    print(result.get("verification_result"))

    print("\nFinal Answer:")
    print(result.get("answer"))