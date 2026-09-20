from services.order_service import (
    get_order_status as fetch_order_status,
    get_complete_order_details,
    cancel_order as cancel_order_service
)
from typing import Optional


# ============================================================
# ORDER STATUS TOOL
# ============================================================

def get_order_status(
    user_id: int,
    order_id: Optional[int] = None
):

    if user_id is None:

        return {
            "found": False,
            "error": "User authentication required."
        }

    return fetch_order_status(
        user_id=user_id,
        order_id=order_id
    )


# ============================================================
# ORDER DETAILS TOOL
# ============================================================

def get_order_details(
    user_id: int,
    order_id: Optional[int] = None
):

    if user_id is None:

        return {
            "found": False,
            "error": "User authentication required."
        }

    return get_complete_order_details(
        user_id=user_id,
        order_id=order_id
    )

# ============================================================
# CANCEL ORDER TOOL
# ============================================================

def cancel_order(
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
            "error": "Order ID is required for cancellation."
        }

    return cancel_order_service(
        user_id=user_id,
        order_id=order_id
    )