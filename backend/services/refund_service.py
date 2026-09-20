from database import get_connection


def process_refund(
    user_id: int,
    order_id: int
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get payment and verify that the order belongs to the user
        select_query = """
            SELECT
                p.id AS payment_id,
                p.order_id,
                p.transaction_id,
                p.amount,
                p.status AS payment_status,
                p.payment_method,
                o.user_id,
                o.status AS order_status
            FROM payments p
            JOIN orders o
                ON p.order_id = o.id
            WHERE p.order_id = %s
              AND o.user_id = %s
            LIMIT 1
        """

        cursor.execute(
            select_query,
            (order_id, user_id)
        )

        payment = cursor.fetchone()

        if not payment:
            return {
                "success": False,
                "message": "Payment not found for this order."
            }

        payment_status = payment["payment_status"]
        order_status = payment["order_status"]

        # ------------------------------------------------
        # Order must be cancelled before refund
        # ------------------------------------------------

        if order_status != "CANCELLED":
            return {
                "success": False,
                "message": (
                    f"Refund cannot be processed because "
                    f"the order is currently {order_status}. "
                    f"The order must be cancelled first."
                ),
                "payment": payment
            }

        # Already refunded
        if payment_status == "REFUNDED":
            return {
                "success": True,
                "already_refunded": True,
                "message": "This payment has already been refunded.",
                "payment": payment
            }

        # Payment failed
        if payment_status == "FAILED":
            return {
                "success": False,
                "message": (
                    "The payment failed, so there is no successful "
                    "payment to refund."
                ),
                "payment": payment
            }

        # Payment still pending
        if payment_status == "PENDING":
            return {
                "success": False,
                "message": (
                    "The payment is still pending. "
                    "A refund cannot be processed yet."
                ),
                "payment": payment
            }

        # Only successful payments can be refunded
        if payment_status != "SUCCESS":
            return {
                "success": False,
                "message": (
                    f"Payment cannot be refunded because its "
                    f"current status is {payment_status}."
                ),
                "payment": payment
            }

        # Update payment status
        update_query = """
            UPDATE payments
            SET status = 'REFUNDED'
            WHERE id = %s
              AND order_id = %s
              AND status = 'SUCCESS'
        """

        cursor.execute(
            update_query,
            (
                payment["payment_id"],
                order_id
            )
        )

        if cursor.rowcount != 1:
            connection.rollback()

            return {
                "success": False,
                "message": (
                    "The refund could not be processed. "
                    "The payment status may have changed."
                )
            }

        connection.commit()

        payment["payment_status"] = "REFUNDED"

        return {
            "success": True,
            "message": "Refund processed successfully.",
            "payment": payment
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()