from tools.payment_tools import get_payment_status
from tools.refund_tools import refund_payment


tests = [
    {
        "user_id": 4,
        "order_id": 2
    },
    {
        "user_id": 5,
        "order_id": 3
    },
    {
        "user_id": 6,
        "order_id": 4
    }
]


for test in tests:

    print("\n")
    print("=" * 70)
    print(
        f"USER ID: {test['user_id']} | "
        f"ORDER ID: {test['order_id']}"
    )
    print("=" * 70)

    print("\nPAYMENT STATUS:")

    result = get_payment_status(
        user_id=test["user_id"],
        order_id=test["order_id"]
    )

    print(result)