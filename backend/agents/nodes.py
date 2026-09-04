from rag.llm import generate_answer
from rag.rag_chain import answer_question

from tools.order_tools import get_order_status
from tools.payment_tools import get_payment_status
from tools.restaurant_tools import get_restaurant_information
from tools.delivery_tools import get_delivery_status
from tools.support_tools import escalate_to_human

from .state import SupportState


def understand_request(
    state: SupportState
) -> SupportState:

    question = state["question"]

    prompt = f"""
You are a customer support intent classifier
for a food delivery application.

Classify the customer's request into exactly
one of these capabilities:

rag
order
payment
restaurant
delivery
human

Definitions:

rag:
General questions about company policies,
refund policies, cancellation policies,
payments policies, etc.

order:
Questions about a specific order, order status,
cancellation, missing items, incorrect items, etc.

payment:
Payment failures, duplicate charges,
deductions, refunds and transaction problems.

restaurant:
Restaurant information, restaurant availability,
food information, restaurant complaints, etc.

delivery:
Delivery partner, delivery tracking,
delivery delays and delivery issues.

human:
Requests that clearly require human support,
serious complaints, disputes, safety issues,
or situations that cannot be automatically resolved.

Return ONLY the capability name.

Customer question:
{question}
"""

    capability = generate_answer(prompt).strip().lower()

    valid_capabilities = {
        "rag",
        "order",
        "payment",
        "restaurant",
        "delivery",
        "human"
    }

    if capability not in valid_capabilities:
        capability = "human"

    state["capability"] = capability

    return state

    # ==========================================================
    # RAG NODE
    # ==========================================================


def rag_node(
state: SupportState
) -> SupportState:

    question = state["question"]

    answer = answer_question(question)

    state["answer"] = answer

    return state

# ==========================================================
# ORDER NODE
# ==========================================================


def order_node(
state: SupportState
) -> SupportState:

    user_id = state.get(
        "user_id"
    )

    if user_id is None:

        state["tool_result"] = {
            "found": False,
            "error": "User authentication required."
        }

        return state

    result = get_order_status(
        user_id
    )

    state["tool_result"] = result

    return state

# ==========================================================
# PAYMENT NODE
# ==========================================================

def payment_node(
    state: SupportState
) -> SupportState:

    result = get_payment_status(1)

    state["tool_result"] = result

    return state


# ==========================================================
# RESTAURANT NODE
# ==========================================================

def restaurant_node(
    state: SupportState
) -> SupportState:

    result = get_restaurant_information(1)

    state["tool_result"] = result

    return state


# ==========================================================
# DELIVERY NODE
# ==========================================================

def delivery_node(
    state: SupportState
) -> SupportState:

    result = get_delivery_status(1)

    state["tool_result"] = result

    return state


# ==========================================================
# HUMAN ESCALATION NODE
# ==========================================================

def human_node(
    state: SupportState
) -> SupportState:

    result = escalate_to_human(
        state["question"]
    )

    state["tool_result"] = result

    state["needs_human"] = True

    return state


# ==========================================================
# VERIFY NODE
# ==========================================================

def verify_node(state: SupportState):

    tool_result = state.get(
        "tool_result"
    )

    if not tool_result:

        state["verification_result"] = (
            "No tool result was returned."
        )

        return state

    if tool_result.get("found") is False:

        state["verification_result"] = (
            tool_result.get(
                "message",
                "No order information found."
            )
        )

        return state

    data = tool_result.get(
        "data"
    )

    if not data:

        state["verification_result"] = (
            "Order data is missing."
        )

        return state

    order = data.get(
        "order"
    )

    items = data.get(
        "items"
    )

    delivery = data.get(
        "delivery"
    )

    if not order:

        state["verification_result"] = (
            "Order information could not be verified."
        )

        return state

    if not items:

        state["verification_result"] = (
            "Order exists but order items "
            "could not be verified."
        )

        return state

    state["verification_result"] = (
        "Order information verified successfully."
    )

    return state   

# ==========================================================
# GENERATE RESPONSE NODE
# ==========================================================

def generate_response(
    state: SupportState
) -> SupportState:

    if state.get("answer"):

        return state

    question = state["question"]

    capability = state.get("capability")

    tool_result = state.get("tool_result")

    verification = state.get(
        "verification_result"
    )

    prompt = f"""
    You are an AI customer support assistant
    for a food delivery application.

    Customer question:
    {question}

    Capability selected:
    {capability}

    Information obtained from the system:
    {tool_result}

    Verification:
    {verification}

    Generate a helpful and concise response.

    Do not invent information.
    Only use the information provided above.
    """

    answer = generate_answer(prompt)

    state["answer"] = answer

    return state

