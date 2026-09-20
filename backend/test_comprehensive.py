from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    # =========================================================
    # 1. RAG
    # =========================================================

    {
        "name": "RAG - General Support Question",
        "question": "What should I do if my food is missing?",
        "user_id": 4
    },


    # =========================================================
    # 2. ORDER
    # =========================================================

    {
        "name": "Order - Track Order",
        "question": "Where is my order?",
        "user_id": 4
    },

    {
        "name": "Order - Order Status",
        "question": "What is the status of my order?",
        "user_id": 4
    },

    {
        "name": "Order - Order Details",
        "question": "Show me the details of my order.",
        "user_id": 4
    },

    {
        "name": "Order - Cancel Order",
        "question": "I want to cancel order 3.",
        "user_id": 5
    },


    # =========================================================
    # 3. PAYMENT
    # =========================================================

    {
        "name": "Payment - Payment Status",
        "question": "What is the payment status of order 2?",
        "user_id": 4
    },

    {
        "name": "Payment - Refund Status",
        "question": "What is the refund status of order 3?",
        "user_id": 5
    },

    {
        "name": "Payment - Refund Request",
        "question": "I want a refund for order 3.",
        "user_id": 5
    },


    # =========================================================
    # 4. RESTAURANT
    # =========================================================

    {
        "name": "Restaurant - Information",
        "question": "Tell me about Pizza Hub.",
        "user_id": 4
    },

    {
        "name": "Restaurant - Dishes",
        "question": "What dishes are available at Pizza Hub?",
        "user_id": 4
    },


    # =========================================================
    # 5. DELIVERY
    # =========================================================

    {
        "name": "Delivery - Delivery Partner",
        "question": "Who is delivering my order?",
        "user_id": 4
    },

    {
        "name": "Delivery - ETA",
        "question": "When will my delivery arrive?",
        "user_id": 4
    },

    {
        "name": "Delivery - Delivery Status",
        "question": "What is the delivery status of my order?",
        "user_id": 4
    },


    # =========================================================
    # 6. HUMAN SUPPORT
    # =========================================================

    {
        "name": "Human - Create Ticket",
        "question": "I need human help with my order.",
        "user_id": 4
    },

    {
        "name": "Human - My Tickets",
        "question": "Show me my support tickets.",
        "user_id": 4
    },

    {
        "name": "Human - Ticket Status",
        "question": "What is the status of support ticket 7?",
        "user_id": 4
    },

    {
        "name": "Human - Update Ticket",
        "question": "Mark support ticket 7 as resolved.",
        "user_id": 4
    }
]


for index, test in enumerate(tests, start=1):

    print("\n")
    print("=" * 80)
    print(f"TEST {index}: {test['name']}")
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

        print("\nRestaurant:")
        print(result.get("restaurant_name"))

        print("\nPayment ID:")
        print(result.get("payment_id"))

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

        print("\n❌ TEST FAILED")
        print("Error:", e)

    import time
    time.sleep(3)