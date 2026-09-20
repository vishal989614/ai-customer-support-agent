from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    # =========================================================
    # ORDER OWNERSHIP
    # =========================================================

    {
        "name": "User 4 accessing User 5's order",
        "question": "Show me the details of order 3.",
        "user_id": 4
    },

    {
        "name": "User 5 accessing User 6's order",
        "question": "What is the status of order 4?",
        "user_id": 5
    },


    # =========================================================
    # PAYMENT OWNERSHIP
    # =========================================================

    {
        "name": "User 4 accessing User 5's payment",
        "question": "What is the payment status of order 3?",
        "user_id": 4
    },

    {
        "name": "User 5 accessing User 6's payment",
        "question": "What is the payment status of order 4?",
        "user_id": 5
    },


    # =========================================================
    # TICKET OWNERSHIP
    # =========================================================

    {
        "name": "User 4 accessing another user's ticket",
        "question": "What is the status of support ticket 7?",
        "user_id": 5
    },

]


for index, test in enumerate(tests, start=1):

    print("\n")
    print("=" * 80)
    print(f"SECURITY TEST {index}: {test['name']}")
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

        print("\nPayment ID:")
        print(result.get("payment_id"))

        print("\nTicket ID:")
        print(result.get("ticket_id"))

        print("\nTool Result:")
        print(result.get("tool_result"))

        print("\nVerification:")
        print(result.get("verification_result"))

        print("\nFinal Answer:")
        print(result.get("answer"))

    except Exception as e:

        print("\n❌ ERROR")
        print(e)