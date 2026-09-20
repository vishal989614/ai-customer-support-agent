from database import get_connection
from typing import Optional

def create_support_ticket(
    user_id: int,
    order_id: Optional[int],
    issue_type: str,
    description: str,
    priority: str = "MEDIUM"
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO support_tickets
        (
            user_id,
            order_id,
            issue_type,
            description,
            priority,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    try:

        cursor.execute(
            query,
            (
                user_id,
                order_id,
                issue_type,
                description,
                priority,
                "OPEN"
            )
        )

        connection.commit()

        ticket_id = cursor.lastrowid

        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": "OPEN",
            "message": "Support ticket created successfully."
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()

def get_support_ticket(
    user_id: int,
    ticket_id: int
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            id,
            user_id,
            order_id,
            issue_type,
            description,
            priority,
            status,
            created_at
        FROM support_tickets
        WHERE id = %s
          AND user_id = %s
        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (ticket_id, user_id)
        )

        ticket = cursor.fetchone()

        if not ticket:
            return {
                "found": False,
                "message": "Support ticket not found."
            }

        return {
            "found": True,
            "ticket": ticket
        }

    finally:

        cursor.close()
        connection.close()

def get_user_support_tickets(
    user_id: int
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            id,
            user_id,
            order_id,
            issue_type,
            description,
            priority,
            status,
            created_at
        FROM support_tickets
        WHERE user_id = %s
        ORDER BY created_at DESC
    """

    try:

        cursor.execute(
            query,
            (user_id,)
        )

        tickets = cursor.fetchall()

        return {
            "found": True,
            "tickets": tickets
        }

    finally:

        cursor.close()
        connection.close()        


def update_support_ticket_status(
    user_id: int,
    ticket_id: int,
    new_status: str
):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    allowed_statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ]

    new_status = new_status.upper()

    if new_status not in allowed_statuses:
        cursor.close()
        connection.close()

        return {
            "success": False,
            "message": (
                f"Invalid ticket status: {new_status}. "
                f"Allowed statuses are: "
                f"{', '.join(allowed_statuses)}."
            )
        }

    try:

        # First verify that the ticket belongs to the user
        select_query = """
            SELECT
                id,
                user_id,
                order_id,
                issue_type,
                description,
                priority,
                status,
                created_at
            FROM support_tickets
            WHERE id = %s
              AND user_id = %s
            LIMIT 1
        """

        cursor.execute(
            select_query,
            (ticket_id, user_id)
        )

        ticket = cursor.fetchone()

        if not ticket:
            return {
                "success": False,
                "found": False,
                "message": "Support ticket not found."
            }

        old_status = ticket["status"]

        # Update status
        update_query = """
            UPDATE support_tickets
            SET status = %s
            WHERE id = %s
              AND user_id = %s
        """

        cursor.execute(
            update_query,
            (
                new_status,
                ticket_id,
                user_id
            )
        )

        connection.commit()

        return {
            "success": True,
            "found": True,
            "ticket_id": ticket_id,
            "old_status": old_status,
            "new_status": new_status,
            "message": (
                f"Support ticket #{ticket_id} "
                f"status updated from {old_status} "
                f"to {new_status}."
            )
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()        
