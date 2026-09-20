from services.refund_service import process_refund


def refund_payment(
    user_id: int,
    order_id: int
):
    if user_id is None:
        return {
            "success": False,
            "error": "User authentication required."
        }

    if order_id is None:
        return {
            "success": False,
            "error": "Order ID is required for refund."
        }

    return process_refund(
        user_id=user_id,
        order_id=order_id
    )