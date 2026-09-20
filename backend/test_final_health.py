from agents.graph import build_support_graph


agent = build_support_graph()


tests = [

    # =========================================================
    # 1. RAG
    # =========================================================

    {
        "name": "RAG",
        "question": "What should I do if my food is missing?",
        "user_id": 4
    },


    # =========================================================
    # 2. ORDER
    # =========================================================

    {
        "name": "ORDER",
        "question": "What is the status of my order?",
        "user_id": 4
    },


    # =========================================================
    # 3. PAYMENT
    # =========================================================

    {
        "name": "PAYMENT",
        "question": "What is the payment status of order 2?",
        "user_id": 4
    },


    # =========================================================
    # 4. RESTAURANT
    # =========================================================

    {
        "name": "RESTAURANT",
        "question": "Tell me about Pizza Hub.",
        "user_id": 4
    },


    # =========================================================
    # 5. DELIVERY
    # =========================================================

    {
        "name": "DELIVERY",
        "question": "What is the delivery status of my order?",
        "user_id": 4
    },


    # =========================================================
    # 6. HUMAN SUPPORT
    # =========================================================

    {
        "name": "HUMAN SUPPORT",
        "question": "What is the status of support ticket 7?",
        "user_id": 4
    }

]


passed = 0
failed = 0


for index, test in enumerate(tests, start=1):

    print("\n")
    print("=" * 80)
    print(f"FINAL HEALTH TEST {index}: {test['name']}")
    print("=" * 80)

    try:

        result = agent.invoke(
            {
                "question": test["question"],
                "user_id": test["user_id"]
            }
        )

        capability = result.get("capability")
        intent = result.get("intent")
        answer = result.get("answer")
        verification = result.get("verification_result")

        print("Question:", test["question"])

        print("\nCapability:")
        print(capability)

        print("\nIntent:")
        print(intent)

        print("\nVerification:")
        print(verification)

        print("\nFinal Answer:")
        print(answer)

        if capability and answer :

            print("\nSTATUS: ✅ PASS")
            passed += 1

        else:

            print("\nSTATUS: ❌ FAIL")
            failed += 1

    except Exception as e:

        print("\nSTATUS: ❌ FAIL")
        print("Error:", e)

        failed += 1


print("\n")
print("=" * 80)
print("FINAL BACKEND HEALTH SUMMARY")
print("=" * 80)

print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\n🎉 BACKEND HEALTH CHECK PASSED")
else:
    print("\n⚠️ SOME TESTS FAILED")