from services.payment_service import (
    get_user_payment_status
)


def get_payment_status(
    user_id: int, order_id: int
):

    if user_id is None:

        return {
            "found": False,
            "error": "User authentication required."
        }

    if order_id is None:
        return {
            "found": False,
            "error": "Order ID is required."
        }

    return get_user_payment_status(
        user_id=user_id,
        order_id=order_id
    )

    