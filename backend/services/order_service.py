from database import get_connection
from typing import Optional

# ============================================================
# GET ACTIVE ORDER FOR USER
# ============================================================

def get_active_order(user_id: int):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            o.id AS order_id,
            o.user_id,
            o.restaurant_id,
            r.name AS restaurant_name,
            o.status AS order_status,
            o.total_amount,
            o.delivery_address,
            o.created_at,
            o.updated_at
        FROM orders o
        JOIN restaurants r
            ON o.restaurant_id = r.id
        WHERE o.user_id = %s
          AND o.status NOT IN ('DELIVERED', 'CANCELLED')
        ORDER BY o.created_at DESC
        LIMIT 1
    """

    try:

        cursor.execute(query, (user_id,))
        order = cursor.fetchone()

        if not order:
            return {
                "found": False,
                "message": "No active order found."
            }

        return {
            "found": True,
            "order": order
        }
    finally:

        cursor.close()
        connection.close()

# ============================================================
# GET ORDER BY ID
# ============================================================        

def get_order_by_id(
    user_id: int,
    order_id: int
):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            o.id AS order_id,
            o.user_id,
            o.restaurant_id,
            r.name AS restaurant_name,
            o.status AS order_status,
            o.total_amount,
            o.delivery_address,
            o.created_at,
            o.updated_at
        FROM orders o
        JOIN restaurants r
            ON o.restaurant_id = r.id
        WHERE o.id = %s
          AND o.user_id = %s
        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (order_id, user_id)
        )

        order = cursor.fetchone()

        if not order:

            return {
                "found": False,
                "message": "Order not found."
            }

        return {
            "found": True,
            "order": order
        }

    finally:

        cursor.close()
        connection.close()

# ============================================================
# GET ORDER ITEMS
# ============================================================

def get_order_items(order_id: int):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            oi.id AS order_item_id,
            oi.order_id,
            oi.dish_id,
            d.name AS dish_name,
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

# ============================================================
# GET COMPLETE ORDER DETAILS
# ============================================================

def get_complete_order_details(
    user_id: int,
    order_id: Optional[int] = None
):

    # --------------------------------------------------------
    # Get order
    # --------------------------------------------------------

    if order_id is not None:

        order_result = get_order_by_id(
            user_id,
            order_id
        )

    else:

        order_result = get_active_order(
            user_id
        )

    if not order_result["found"]:

        return order_result

    order = order_result["order"]

    # --------------------------------------------------------
    # Get items
    # --------------------------------------------------------

    items = get_order_items(
        order["order_id"]
    )

    return {
        "found": True,
        "order": order,
        "items": items
    }


# ============================================================
# GET ORDER STATUS
# ============================================================

def get_order_status(
    user_id: int,
    order_id: Optional[int] = None
):

    if order_id is not None:

        result = get_order_by_id(
            user_id,
            order_id
        )

    else:

        result = get_active_order(
            user_id
        )

    return result    


def cancel_order(
    user_id: int,
    order_id: int
):
    """
    Cancel an order only if it belongs to the user
    and is still in a cancellable state.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # ====================================================
        # STEP 1: Find the order
        # ====================================================

        select_query = """
            SELECT
                o.id AS order_id,
                o.user_id,
                o.status AS order_status,
                o.total_amount,
                r.name AS restaurant_name
            FROM orders o
            JOIN restaurants r
                ON o.restaurant_id = r.id
            WHERE o.id = %s
              AND o.user_id = %s
            LIMIT 1
        """

        cursor.execute(
            select_query,
            (order_id, user_id)
        )

        order = cursor.fetchone()

        if not order:

            return {
                "success": False,
                "message": "Order not found."
            }

        # ====================================================
        # STEP 2: Check current status
        # ====================================================

        current_status = order["order_status"]

        cancellable_statuses = {
            "PLACED",
            "CONFIRMED",
            "PREPARING"
        }

        if current_status not in cancellable_statuses:

            return {
                "success": False,
                "message": (
                    f"Order cannot be cancelled because "
                    f"its current status is {current_status}."
                ),
                "order": order
            }

        # ====================================================
        # STEP 3: Cancel order
        # ====================================================

        update_query = """
            UPDATE orders
            SET
                status = 'CANCELLED',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
              AND user_id = %s
              AND status IN (
                  'PLACED',
                  'CONFIRMED',
                  'PREPARING'
              )
        """

        cursor.execute(
            update_query,
            (order_id, user_id)
        )

        # ====================================================
        # STEP 4: Make sure update actually happened
        # ====================================================

        if cursor.rowcount != 1:

            connection.rollback()

            return {
                "success": False,
                "message": (
                    "The order could not be cancelled. "
                    "Its status may have changed."
                )
            }

        # ====================================================
        # STEP 5: Commit
        # ====================================================

        connection.commit()

        # ====================================================
        # STEP 6: Return cancellation result
        # ====================================================

        order["order_status"] = "CANCELLED"

        return {
            "success": True,
            "message": "Order cancelled successfully.",
            "order": order
        }

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()


