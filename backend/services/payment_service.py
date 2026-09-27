from database import get_connection


def get_user_payment_status(user_id: int, order_id: int = None):
    

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    if order_id is not None:
        query = """
            SELECT
                p.id AS payment_id,
                p.order_id,
                p.transaction_id,
                p.amount,
                p.status AS payment_status,
                p.payment_method,
                p.created_at,
                o.status AS order_status,
                o.restaurant_id,
                r.name AS restaurant_name
            FROM payments p
            JOIN orders o
                ON p.order_id = o.id
            LEFT JOIN restaurants r
                ON o.restaurant_id = r.id
            WHERE p.order_id = %s
              AND o.user_id = %s
            LIMIT 1
        """
        params = (order_id, user_id)
    else:
        query = """
            SELECT
                p.id AS payment_id,
                p.order_id,
                p.transaction_id,
                p.amount,
                p.status AS payment_status,
                p.payment_method,
                p.created_at,
                o.status AS order_status,
                o.restaurant_id,
                r.name AS restaurant_name
            FROM payments p
            JOIN orders o
                ON p.order_id = o.id
            LEFT JOIN restaurants r
                ON o.restaurant_id = r.id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC, p.id DESC
            LIMIT 1
        """
        params = (user_id,)

    try:
        cursor.execute(query, params)
        payment = cursor.fetchone()

        if not payment:

            return {
                "found": False,
                "message": "No payment information found."
            }

        return {
            "found": True,
            "payment": payment
        }

    finally:

        cursor.close()
        connection.close()