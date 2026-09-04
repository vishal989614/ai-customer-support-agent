from typing import Any, TypedDict


class SupportState(TypedDict, total=False):

    question: str

    user_id: int

    capability: str

    context: list[str]

    tool_result: Any

    verification_result: str

    answer: str

    needs_human: bool