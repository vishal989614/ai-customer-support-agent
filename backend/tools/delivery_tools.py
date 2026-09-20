from services.delivery_service import (
    get_user_delivery_status
)


def get_delivery_status(
    user_id: int
):

    if user_id is None:

        return {
            "found": False,
            "error": (
                "User authentication required."
            )
        }

    return get_user_delivery_status(
        user_id
    )