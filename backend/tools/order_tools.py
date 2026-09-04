from services.order_service import (
    get_complete_order_details
)


def get_order_status(user_id: int):

    result = get_complete_order_details(
        user_id
    )

    if result is None:

        return {
            "found": False,
            "message": "No active order found."
        }

    return {
        "found": True,
        "data": result
    }