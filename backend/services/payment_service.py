from database import get_connection


def get_user_payment_status(user_id: int, order_id: int = None):
    

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

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
            o.restaurant_id

        FROM payments p

        JOIN orders o
            ON p.order_id = o.id

        WHERE p.order_id = %s
          AND o.user_id = %s

        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (order_id, user_id)
        )

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