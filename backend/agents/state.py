from typing import Any, TypedDict


class SupportState(TypedDict, total=False):

   # User input
    question: str
    user_id: int

    # Structured understanding
    capability: str
    intent: str

    # Extracted entities
    order_id: int
    restaurant_id: int
    restaurant_name: str
    payment_id: int
    ticket_id: int

    issue_type: str
    priority: str
    new_status: str

    # Agent processing
    context: list[str]
    tool_result: Any
    verification_result: str
    answer: str

    # Human escalation
    needs_human: bool