from agents.graph import build_support_graph


agent = build_support_graph()


questions = [

    "Where is my order?",

    "What is the status of my payment?",

    "Tell me about Spice Garden",

    "Show me the menu of Pizza Hub",

    "Who is delivering my order?",

    "What is your refund policy?",

    "I want to talk to a human"
]


for question in questions:

    print("\n========================================")
    print("QUESTION:", question)
    print("========================================")

    result = agent.invoke(
        {
            "question": question,
            "user_id": 4
        }
    )

    print("Capability:", result.get("capability"))
    print("Intent:", result.get("intent"))
    print("Order ID:", result.get("order_id"))
    print("Restaurant:", result.get("restaurant_name"))
    print("Payment ID:", result.get("payment_id"))
    print("Answer:", result.get("answer"))