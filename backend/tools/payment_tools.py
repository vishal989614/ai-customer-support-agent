from typing import Optional
from services.payment_service import (
    get_user_payment_status
)


def get_payment_status(
    user_id: int, order_id: Optional[int] = None
):

    if user_id is None:

        return {
            "found": False,
            "error": "User authentication required."
        }

    return get_user_payment_status(
        user_id=user_id,
        order_id=order_id
    )


    