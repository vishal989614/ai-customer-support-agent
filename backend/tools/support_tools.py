from typing import Optional

from services.support_service import (
    create_support_ticket,
    get_support_ticket,
    get_user_support_tickets,
    update_support_ticket_status
)


def escalate_to_human(
    user_id: int,
    order_id: Optional[int],
    issue_type: str,
    description: str,
    priority: str = "MEDIUM"
):

    if user_id is None:
        return {
            "success": False,
            "error": "User authentication required."
        }

    if not description:
        return {
            "success": False,
            "error": "Issue description is required."
        }

    return create_support_ticket(
        user_id=user_id,
        order_id=order_id,
        issue_type=issue_type,
        description=description,
        priority=priority
    )

def get_ticket(
    user_id: int,
    ticket_id: int
):

    if user_id is None:
        return {
            "found": False,
            "error": "User authentication required."
        }

    if ticket_id is None:
        return {
            "found": False,
            "error": "Ticket ID is required."
        }

    return get_support_ticket(
        user_id=user_id,
        ticket_id=ticket_id
    )

def get_my_tickets(
    user_id: int
):

    if user_id is None:
        return {
            "found": False,
            "error": "User authentication required."
        }

    return get_user_support_tickets(
        user_id=user_id
    )

def update_ticket_status(
    user_id: int,
    ticket_id: int,
    new_status: str
):
    if user_id is None:
        return {
            "success": False,
            "error": "User authentication required."
        }

    if ticket_id is None:
        return {
            "success": False,
            "error": "Ticket ID is required."
        }

    if not new_status:
        return {
            "success": False,
            "error": "New ticket status is required."
        }

    return update_support_ticket_status(
        user_id=user_id,
        ticket_id=ticket_id,
        new_status=new_status
    )