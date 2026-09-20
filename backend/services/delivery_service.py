from database import get_connection


# ==========================================================
# FIND USER'S ACTIVE ORDER
# ==========================================================

def get_active_order_for_user(
    user_id: int
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            o.id AS order_id,
            o.user_id,
            o.restaurant_id,
            o.status AS order_status,
            o.total_amount,
            o.delivery_address,
            o.created_at,
            r.name AS restaurant_name

        FROM orders o

        JOIN restaurants r
            ON o.restaurant_id = r.id

        WHERE o.user_id = %s

        AND o.status NOT IN (
            'DELIVERED',
            'CANCELLED'
        )

        ORDER BY o.created_at DESC

        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (user_id,)
        )

        order = cursor.fetchone()

        return order

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# GET DELIVERY FOR ORDER
# ==========================================================

def get_delivery_for_order(
    order_id: int
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            order_id,
            status,
            delivery_partner_name,
            delivery_partner_phone,
            estimated_delivery_time,
            delivered_at

        FROM deliveries

        WHERE order_id = %s

        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (order_id,)
        )

        delivery = cursor.fetchone()

        return delivery

    finally:

        cursor.close()
        connection.close()


# ==========================================================
# COMPLETE DELIVERY INFORMATION
# ==========================================================

def get_user_delivery_status(
    user_id: int
):

    # ------------------------------------------
    # Find active order
    # ------------------------------------------

    order = get_active_order_for_user(
        user_id
    )

    if not order:

        return {
            "found": False,
            "message": "No active order found."
        }

    order_id = order[
        "order_id"
    ]

    # ------------------------------------------
    # Find delivery
    # ------------------------------------------

    delivery = get_delivery_for_order(
        order_id
    )

    if not delivery:

        return {
            "found": False,
            "message": (
                "No delivery information "
                "is available for your active order."
            ),
            "order": order
        }

    # ------------------------------------------
    # Return combined information
    # ------------------------------------------

    return {
        "found": True,

        "order": order,

        "delivery": delivery
    }