from database import get_connection


def get_active_order(user_id: int):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            o.id,
            o.user_id,
            o.restaurant_id,
            o.status,
            o.total_amount,
            o.delivery_address,
            o.created_at,

            r.name AS restaurant_name,
            r.address AS restaurant_address,
            r.rating AS restaurant_rating

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

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


def get_order_items(order_id: int):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            oi.dish_id,
            d.name AS dish_name,
            d.description,
            d.category,
            oi.quantity,
            oi.price

        FROM order_items oi

        JOIN dishes d
            ON oi.dish_id = d.id

        WHERE oi.order_id = %s

        ORDER BY oi.id
    """

    try:

        cursor.execute(
            query,
            (order_id,)
        )

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


def get_delivery_status(order_id: int):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            status,
            delivery_partner_name,
            delivery_partner_phone,
            estimated_delivery_time,
            delivered_at

        FROM deliveries

        WHERE order_id = %s
    """

    try:

        cursor.execute(
            query,
            (order_id,)
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()


def get_complete_order_details(user_id: int):

    order = get_active_order(user_id)

    if not order:

        return None

    order_id = order["id"]

    items = get_order_items(
        order_id
    )

    delivery = get_delivery_status(
        order_id
    )

    return {
        "order": order,
        "items": items,
        "delivery": delivery
    }