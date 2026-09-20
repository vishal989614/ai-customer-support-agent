from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    # =========================================================
    # ORDER EDGE CASES
    # =========================================================

    {
        "name": "Cancel out-for-delivery order",
        "question": "Cancel order 2",
        "user_id": 4
    },

    {
        "name": "Cancel delivered order",
        "question": "Cancel order 4",
        "user_id": 6
    },

    {
        "name": "Cancel already-cancelled order",
        "question": "Cancel order 3",
        "user_id": 5
    },


    # =========================================================
    # PAYMENT / REFUND EDGE CASES
    # =========================================================

    {
        "name": "Refund out-for-delivery order",
        "question": "I want a refund for order 2.",
        "user_id": 4
    },

    {
        "name": "Refund delivered order",
        "question": "I want a refund for order 4.",
        "user_id": 6
    },

    {
        "name": "Refund already-refunded payment",
        "question": "I want a refund for order 3.",
        "user_id": 5
    },


    # =========================================================
    # SUPPORT TICKET EDGE CASES
    # =========================================================

    {
        "name": "Invalid ticket status",
        "question": "Mark support ticket 7 as INVALID.",
        "user_id": 4
    },

    {
        "name": "Nonexistent ticket",
        "question": "Mark support ticket 999 as resolved.",
        "user_id": 4
    },

    {
        "name": "Nonexistent ticket status",
        "question": "What is the status of support ticket 999?",
        "user_id": 4
    }

]


for index, test in enumerate(tests, start=1):

    print("\n")
    print("=" * 80)
    print(f"EDGE CASE TEST {index}: {test['name']}")
    print("=" * 80)

    print("Question:", test["question"])
    print("User ID:", test["user_id"])

    try:

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

        print("\nTicket ID:")
        print(result.get("ticket_id"))

        print("\nNew Status:")
        print(result.get("new_status"))

        print("\nTool Result:")
        print(result.get("tool_result"))

        print("\nVerification:")
        print(result.get("verification_result"))

        print("\nFinal Answer:")
        print(result.get("answer"))

    except Exception as e:

        print("\n❌ ERROR")
        print("Error:", e)