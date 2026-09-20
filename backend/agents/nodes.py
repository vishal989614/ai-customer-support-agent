import json

from rag.llm import generate_answer
from rag.rag_chain import answer_question

from tools.order_tools import (
    get_order_status, 
    get_order_details,
    cancel_order
)
from tools.payment_tools import get_payment_status
from tools.restaurant_tools import (
    get_restaurant_information,
    get_restaurant_by_name
)
from tools.delivery_tools import get_delivery_status
from tools.support_tools import (
    escalate_to_human,
    get_ticket,
    get_my_tickets,
    update_ticket_status
)
from tools.refund_tools import refund_payment

from .state import SupportState


# ============================================================
# 1. UNDERSTAND REQUEST
# ============================================================

def understand_request(state: SupportState) -> SupportState:

    question = state["question"]

    prompt = f"""
You are an intent classification system for a food delivery
customer support application.

Classify the user's request into exactly ONE capability
and exactly ONE intent.

Return ONLY valid JSON.
Do not return markdown.
Do not return explanations.

CAPABILITIES:

rag:
- General support questions
- FAQ
- Cancellation policy
- Refund policy
- Payment policy
- Delivery policy

order:
- Track order
- Order status
- Order details
- Cancel order

payment:
- Payment status
- Refund status
- Refund request
- Payment problems

restaurant:
- Restaurant information
- Restaurant menu
- Restaurant rating
- Restaurant address
- Restaurant availability

delivery:
- Delivery status
- Delivery partner
- Estimated delivery time

human:
- Human support
- Support ticket operations
- Complaints
- Issues requiring human support


RAG INTENTS (General FAQ, policies, and guidance questions):

"What should I do if my food is missing?"
→ capability = "rag"
→ intent = "faq"

"What is your cancellation policy?"
→ capability = "rag"
→ intent = "faq"

"What is your refund policy?"
→ capability = "rag"
→ intent = "faq"

"What happens if my delivery is late?"
→ capability = "rag"
→ intent = "faq"

"What payment methods do you accept?"
→ capability = "rag"
→ intent = "faq"

IMPORTANT DISTINCTION:
- If the user asks a general policy, FAQ, or "what should I do if..." question, use capability = "rag".
- Use capability = "human" ONLY when the user explicitly requests a human agent ("talk to human", "human help"), creates a support ticket, or checks/updates support tickets.


ORDER INTENTS:

"Where is my order?"
→ capability = "order"
→ intent = "track_order"

"What is my order status?"
→ capability = "order"
→ intent = "order_status"

"I want to cancel order 3"
→ capability = "order"
→ intent = "cancel_order"


PAYMENT INTENTS:

"What is my payment status for order 3?"
→ capability = "payment"
→ intent = "payment_status"
→ order_id = 3

"I want a refund for order 3"
→ capability = "payment"
→ intent = "refund_request"
→ order_id = 3

"Has my payment been refunded?"
→ capability = "payment"
→ intent = "refund_status"


RESTAURANT INTENTS:

"Tell me about Spice Garden"
→ capability = "restaurant"
→ intent = "restaurant_information"

"Show me Pizza Hub menu"
→ capability = "restaurant"
→ intent = "restaurant_menu"


DELIVERY INTENTS:

"Who is delivering my order?"
→ capability = "delivery"
→ intent = "delivery_partner"

"When will my delivery arrive?"
→ capability = "delivery"
→ intent = "delivery_eta"

"What is my delivery status?"
→ capability = "delivery"
→ intent = "delivery_status"


SUPPORT TICKET INTENTS:

If the user wants human support or wants to create a ticket:

"I need human help"
→ capability = "human"
→ intent = "human_escalation"

"I want to speak to a human"
→ capability = "human"
→ intent = "human_escalation"

"I have a problem with my order"
→ capability = "human"
→ intent = "human_escalation"


If the user wants to view one specific ticket:

"What is the status of support ticket 7?"
→ capability = "human"
→ intent = "ticket_status"
→ ticket_id = 7

"Tell me about ticket 7"
→ capability = "human"
→ intent = "ticket_status"
→ ticket_id = 7


If the user wants to see all their tickets:

"Show my support tickets"
→ capability = "human"
→ intent = "my_tickets"


IMPORTANT SUPPORT TICKET STATUS UPDATE:

If the user wants to CHANGE the status of an existing
support ticket, use:

→ capability = "human"
→ intent = "update_ticket"

Examples:

"Mark support ticket 7 as resolved"
→ ticket_id = 7
→ new_status = "RESOLVED"

"Resolve ticket 7"
→ ticket_id = 7
→ new_status = "RESOLVED"

"Move ticket 7 to in progress"
→ ticket_id = 7
→ new_status = "IN_PROGRESS"

"Put ticket 7 in progress"
→ ticket_id = 7
→ new_status = "IN_PROGRESS"

"Close support ticket 7"
→ ticket_id = 7
→ new_status = "CLOSED"

"Close ticket 7"
→ ticket_id = 7
→ new_status = "CLOSED"

"Reopen support ticket 7"
→ ticket_id = 7
→ new_status = "OPEN"

Allowed new_status values:

OPEN
IN_PROGRESS
RESOLVED
CLOSED

For update_ticket, ALWAYS extract ticket_id
and new_status when they are present.

Do not classify a status update as ticket_status.

For example:

"Mark ticket 7 as resolved"
must be:

capability = "human"
intent = "update_ticket"

NOT:

intent = "ticket_status"


HUMAN ESCALATION:

If creating a new support ticket, determine:

issue_type:
- PAYMENT_ISSUE
- ORDER_ISSUE
- DELIVERY_ISSUE
- RESTAURANT_ISSUE
- ACCOUNT_ISSUE
- GENERAL_SUPPORT

priority:
- LOW
- MEDIUM
- HIGH

If capability is not human, use null
for issue_type and priority.


Return EXACTLY this JSON structure:

{{
    "capability": null,
    "intent": null,
    "order_id": null,
    "restaurant_id": null,
    "restaurant_name": null,
    "payment_id": null,
    "ticket_id": null,
    "issue_type": null,
    "priority": null,
    "new_status": null
}}

Rules:

- capability must be one of:
  rag, order, payment, restaurant, delivery, human

- Extract IDs as integers.

- Extract restaurant names when present.

- Extract ticket_id when a ticket number is mentioned.

- Extract new_status for update_ticket.

- Return JSON only.

User question:

{question}
"""

    try:

        response = generate_answer(prompt)

        response = response.strip()

        # Remove markdown code fences if Gemini returns them
        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        data = json.loads(response)

        # ------------------------------------------------
        # Store Gemini result
        # ------------------------------------------------

        state["capability"] = data.get("capability", "human")
        state["intent"] = data.get("intent", "")

        state["order_id"] = data.get("order_id")
        state["restaurant_id"] = data.get("restaurant_id")
        state["restaurant_name"] = data.get("restaurant_name")
        state["payment_id"] = data.get("payment_id")

        state["ticket_id"] = data.get("ticket_id")

        state["issue_type"] = data.get("issue_type")
        state["priority"] = data.get("priority")

        state["new_status"] = data.get("new_status")

        # ------------------------------------------------
        # DETERMINISTIC SUPPORT TICKET STATUS HANDLING
        # ------------------------------------------------

        question_lower = question.lower()

        status_update_words = [
            "resolve",
            "resolved",
            "in progress",
            "close",
            "closed",
            "reopen",
            "reopened"
        ]

        is_status_update = any(
            word in question_lower
            for word in status_update_words
        )

        if is_status_update:

            # Status update is ALWAYS a human capability
            state["capability"] = "human"
            state["intent"] = "update_ticket"

            # --------------------------------------------
            # Extract ticket ID if Gemini missed it
            # --------------------------------------------

            if state.get("ticket_id") is None:

                import re

                match = re.search(
                    r"(?:ticket|support ticket)\s*#?\s*(\d+)",
                    question_lower
                )

                if match:
                    state["ticket_id"] = int(
                        match.group(1)
                    )

            # --------------------------------------------
            # Determine status from user's words
            # --------------------------------------------

            if "in progress" in question_lower:

                state["new_status"] = "IN_PROGRESS"

            elif (
                "reopen" in question_lower
                or "reopened" in question_lower
            ):

                state["new_status"] = "OPEN"

            elif (
                "resolved" in question_lower
                or "resolve" in question_lower
            ):

                state["new_status"] = "RESOLVED"

            elif (
                "closed" in question_lower
                or "close" in question_lower
            ):

                state["new_status"] = "CLOSED"

        return state

    except Exception as e:

        print("Intent parsing error:", e)

        state["capability"] = "human"
        state["intent"] = "human_support"

        state["ticket_id"] = None
        state["new_status"] = None

        return state

# ============================================================
# 2. RAG NODE
# ============================================================

def rag_node(state: SupportState) -> SupportState:

    question = state["question"]

    result = answer_question(question)

    state["answer"] = result

    return state


# ============================================================
# 3. ORDER NODE
# ============================================================

def order_node(state: SupportState) -> SupportState:

    user_id = state.get("user_id")
    order_id = state.get("order_id")
    intent = state.get("intent")

    # --------------------------------------------------------
    # Authentication check
    # --------------------------------------------------------

    if user_id is None:

        state["tool_result"] = {
            "found": False,
            "error": "User authentication required."
        }

        return state

    # --------------------------------------------------------
    # Track order
    # --------------------------------------------------------

    if intent == "track_order":

        result = get_order_status(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # Order status
    # --------------------------------------------------------

    if intent == "order_status":

        result = get_order_status(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # Order details
    # --------------------------------------------------------

    if intent == "order_details":

        result = get_order_details(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # Cancel order
    # --------------------------------------------------------

    if intent == "cancel_order":

        # Specific order ID is required for safe cancellation.
        if order_id is None:

            state["tool_result"] = {
                "success": False,
                "confirmation_required": True,
                "message": (
                    "Please provide the order ID "
                    "you want to cancel."
                )
            }

            return state

        result = cancel_order(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # Unsupported order intent
    # --------------------------------------------------------

    state["tool_result"] = {
        "found": False,
        "error": "Unsupported order request."
    }

    return state


# ============================================================
# 4. PAYMENT NODE
# ============================================================

def payment_node(state: SupportState) -> SupportState:

    user_id = state.get("user_id")
    order_id = state.get("order_id")
    intent = state.get("intent")

    if user_id is None:

        state["tool_result"] = {
            "found": False,
            "error": "User authentication required."
        }   
        return state

    if order_id is None:
        state["tool_result"] = {
            "found": False,
            "error": "Order ID is required."
        }
        return state

    # -----------------------------
    # PAYMENT STATUS
    # -----------------------------

    if intent == "payment_status":

        result = get_payment_status(
            user_id=user_id,
            order_id=order_id
            )

        state["tool_result"] = result

        return state

    # -----------------------------
    # REFUND STATUS
    # -----------------------------

    if intent == "refund_status":

        result = get_payment_status(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # -----------------------------
    # REFUND REQUEST
    # -----------------------------

    if intent == "refund_request":

        result = refund_payment(
            user_id=user_id,
            order_id=order_id
        )

        state["tool_result"] = result

        return state

    # -----------------------------
    # UNKNOWN PAYMENT REQUEST
    # -----------------------------

    state["tool_result"] = {
        "found": False,
        "error": "Unsupported payment request."
    }

    return state


# ============================================================
# 5. RESTAURANT NODE
# ============================================================

def restaurant_node(state: SupportState) -> SupportState:

    restaurant_name = state.get("restaurant_name")
    restaurant_id = state.get("restaurant_id")

    # --------------------------------------------------------
    # Search by restaurant name
    # --------------------------------------------------------

    if restaurant_name:

        result = get_restaurant_by_name(
            restaurant_name
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # Search by restaurant ID
    # --------------------------------------------------------

    if restaurant_id:

        result = get_restaurant_information(
            restaurant_id
        )

        state["tool_result"] = result

        return state

    # --------------------------------------------------------
    # No restaurant specified
    # --------------------------------------------------------

    state["tool_result"] = {
        "found": False,
        "error": "Restaurant name or restaurant ID is required."
    }

    return state


# ============================================================
# 6. DELIVERY NODE
# ============================================================

def delivery_node(state: SupportState) -> SupportState:

    user_id = state.get("user_id")

    if user_id is None:

        state["tool_result"] = {
            "found": False,
            "error": "User authentication required."
        }

        return state

    result = get_delivery_status(user_id)

    state["tool_result"] = result

    return state


# ============================================================
# 7. HUMAN NODE
# ============================================================
def human_node(state: SupportState) -> SupportState:

    user_id = state.get("user_id")
    order_id = state.get("order_id") 
    ticket_id = state.get("ticket_id")
    question = state.get("question")

    intent = state.get("intent")

    if user_id is None:
    
        state["tool_result"] = {
            "success": False,
            "error": "User authentication required."
        }

        return state
    
    # 1. CREATE SUPPORT TICKET

    if intent == "human_escalation":

        issue_type = state.get(
            "issue_type",
            "GENERAL_SUPPORT"
        )

        priority = state.get(
            "priority",
            "MEDIUM"
        )
        
        result = escalate_to_human(
            user_id=user_id,
            order_id=order_id,
            issue_type=issue_type,
            description=question,
            priority=priority
        )

        state["tool_result"] = result

        return state

    # 2. GET SPECIFIC TICKET

    if intent == "ticket_status":

        result = get_ticket(
            user_id=user_id,
            ticket_id=ticket_id
        )

        state["tool_result"] = result

        return state

    # 3. GET USER'S TICKETS

    if intent == "my_tickets":

        result = get_my_tickets(
            user_id=user_id
        )

        state["tool_result"] = result

        return state


    # 4. UPDATE TICKET
    if intent == "update_ticket":

        new_status = state.get("new_status")

        if ticket_id is None:
            state["tool_result"] = {
                "success": False,
                "error": "Ticket ID is required."
            }
            return state

        if new_status is None:
            state["tool_result"] = {
                "success": False,
                "error": "New ticket status is required."
            }
            return state

        result = update_ticket_status(
            user_id=user_id,
            ticket_id=ticket_id,
            new_status=new_status
        )

        state["tool_result"] = result
        return state

    # UNKNOWN SUPPORT REQUEST
    
    state["tool_result"] = {
        "found": False,
        "error": "Unsupported support request."
    }

    return state

# ============================================================
# 8. VERIFY NODE
# ============================================================

def verify_node(state: SupportState) -> SupportState:

    capability = state.get("capability")
    intent = state.get("intent")
    result = state.get("tool_result")

    # --------------------------------------------------------
    # ORDER
    # --------------------------------------------------------

    if capability == "order":
        # ========================================================
        # CANCEL ORDER
        # ========================================================

        if state.get("intent") == "cancel_order":

            if not result:

                state["verification_result"] = (
                    "Order cancellation verification failed."
                )

                return state

            # ----------------------------------------------------
            # Cancellation was successful
            # ----------------------------------------------------

            if result.get("success"):

                order = result.get("order")

                if not order:

                    state["verification_result"] = (
                        "Cancellation succeeded but "
                        "order information is missing."
                    )

                    return state

                if order.get("order_status") != "CANCELLED":

                    state["verification_result"] = (
                        "Cancellation could not be verified."
                    )

                    return state

                state["verification_result"] = (
                    "Order cancellation verified successfully."
                )

                return state

            # ----------------------------------------------------
            # Cancellation failed
            # ----------------------------------------------------

            state["verification_result"] = result.get(
                "message",
                result.get(
                    "error",
                    "Order cancellation was not completed."
                )
            )

            return state

        # ========================================================
        # NORMAL ORDER OPERATIONS
        # ========================================================

        if not result:

            state["verification_result"] = (
                "Order verification failed."
            )

            return state

        if not result.get("found"):

            state["verification_result"] = (
                result.get(
                    "message",
                    "No order information found."
                )
            )

            return state

        order = result.get("order")

        if not order:

            state["verification_result"] = (
                "Order information is incomplete."
            )

            return state

        required_fields = [
            "order_id",
            "order_status",
            "restaurant_name",
            "total_amount"
        ]

        for field in required_fields:

            if field not in order:

                state["verification_result"] = (
                    f"Order information missing: {field}"
                )

                return state

        # --------------------------------------------------------
        # Details request
        # --------------------------------------------------------

        if state.get("intent") == "order_details":

            items = result.get("items")

            if items is None:

                state["verification_result"] = (
                    "Order items information is missing."
                )

                return state

        state["verification_result"] = (
            "Order information verified successfully."
        )

        return state

    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    if capability == "payment":

        if not result:
            state["verification_result"] = (
                "Payment verification failed."
            )
            return state

        # ----------------------------------------------------
        # Check whether payment information was found
        # ----------------------------------------------------

        if not result.get("found"):

            # Refund tool uses "success" instead of "found"
            if intent == "refund_request":

                if result.get("success") is not True:
                    state["verification_result"] = (
                        result.get(
                            "message",
                            "Refund could not be processed."
                        )
                    )
                    return state

            else:

                state["verification_result"] = (
                    result.get(
                        "message",
                        "No payment information found."
                    )
                )
                return state

        payment = result.get("payment")    

        # ----------------------------------------------------
        # Payment information must exist
        # ----------------------------------------------------

        if not payment:
            state["verification_result"] = (
                "Payment information is incomplete."
            )
            return state

        required_fields = [
            "payment_id",
            "order_id",
            "amount",
            "payment_status"
        ]

        for field in required_fields:

            if field not in payment:
                state["verification_result"] = (
                    f"Payment information missing: {field}"
                )
                return state

        # ----------------------------------------------------
        # REFUND REQUEST
        # ----------------------------------------------------

        if intent == "refund_request":

            if result.get("success") is not True:
                state["verification_result"] = (
                    result.get(
                        "message",
                        "Refund could not be processed."
                    )
                )
                return state

            if payment.get("payment_status") != "REFUNDED":
                state["verification_result"] = (
                    "Refund could not be verified."
                )
                return state

            state["verification_result"] = (
                "Refund successfully processed and verified. "
                "Payment status is REFUNDED."
            )

            return state

        # ----------------------------------------------------
        # REFUND STATUS
        # ----------------------------------------------------

        if intent == "refund_status":

            payment_status = payment.get("payment_status")

            if payment_status == "REFUNDED":

                state["verification_result"] = (
                    "Refund status verified. "
                    "Payment has been refunded."
                )

            else:

                state["verification_result"] = (
                    f"Refund status verified. "
                    f"Current payment status is {payment_status}."
                )

            return state

        # ----------------------------------------------------
        # NORMAL PAYMENT STATUS
        # ----------------------------------------------------

        if intent == "payment_status":

            state["verification_result"] = (
                "Payment information successfully verified."
            )

            return state

        # ----------------------------------------------------
        # UNKNOWN PAYMENT INTENT
        # ----------------------------------------------------

        state["verification_result"] = (
            "Unsupported payment request."
        )

        return state    


    # --------------------------------------------------------
    # RESTAURANT
    # --------------------------------------------------------

    if capability == "restaurant":

        if not result:
            state["verification_result"] = (
                "Restaurant verification failed."
            )
            return state

        if not result.get("found"):

            state["verification_result"] = (
                result.get(
                    "message",
                    "Restaurant not found."
                )
            )

            return state

        if not result.get("restaurant"):

            state["verification_result"] = (
                "Restaurant information is incomplete."
            )

            return state

        restaurant = result["restaurant"]

        if "id" not in restaurant:
            state["verification_result"] = (
                "Restaurant ID is missing."
            )
            return state

        if "name" not in restaurant:
            state["verification_result"] = (
                "Restaurant name is missing."
            )
            return state

        state["verification_result"] = (
            "Restaurant information verified successfully."
        )

        return state

    # --------------------------------------------------------
    # DELIVERY
    # --------------------------------------------------------

    if capability == "delivery":

        if not result:

            state["verification_result"] = (
                "Delivery verification failed."
            )

            return state

        if not result.get("found"):

            state["verification_result"] = (
                result.get(
                    "message",
                    "Delivery information not found."
                )
            )

            return state

        order = result.get("order")
        delivery = result.get("delivery")

        if not order or not delivery:

            state["verification_result"] = (
                "Delivery information is incomplete."
            )

            return state

        if "order_id" not in order:

            state["verification_result"] = (
                "Order ID is missing from delivery information."
            )

            return state

        if "status" not in delivery:

            state["verification_result"] = (
                "Delivery status is missing."
            )

            return state

        state["verification_result"] = (
            "Delivery information verified successfully."
        )

        return state

    # --------------------------------------------------------
    # HUMAN ESCALATION
    # --------------------------------------------------------

    if capability == "human":

        if not result:

            state["verification_result"] = (
                "Human escalation failed."
            )

            return state

        # ----------------------------------------------------
        # CREATE TICKET
        # ----------------------------------------------------

        if intent == "human_escalation":

            if result.get("success") is not True:

                state["verification_result"] = (
                    result.get(
                        "error",
                        result.get(
                            "message",
                            "Support ticket could not be created."
                        )
                    )
                )

                return state

            created_ticket_id = result.get("ticket_id")
            status = result.get("status")

            if created_ticket_id is None:

                state["verification_result"] = (
                    "Support ticket was created but "
                    "ticket ID is missing."
                )

                return state

            if status != "OPEN":

                state["verification_result"] = (
                    f"Support ticket status could not "
                    f"be verified. Current status: {status}"
                )

                return state

            state["verification_result"] = (
                f"Support ticket #{created_ticket_id} "
                f"created successfully."
            )

            return state

        # ----------------------------------------------------
        # SPECIFIC TICKET
        # ----------------------------------------------------

        if intent == "ticket_status":

            if result.get("found") is not True:

                state["verification_result"] = (
                    result.get(
                        "message",
                        "Support ticket not found."
                    )
                )

                return state

            ticket = result.get("ticket")

            if not ticket:

                state["verification_result"] = (
                    "Support ticket information is missing."
                )

                return state

            required_fields = [
                "id",
                "user_id",
                "status",
                "priority",
                "issue_type"
            ]

            for field in required_fields:

                if field not in ticket:

                    state["verification_result"] = (
                        f"Support ticket information "
                        f"missing: {field}"
                    )

                    return state

            state["verification_result"] = (
                "Support ticket information successfully verified."
            )

            return state

        # ----------------------------------------------------
        # USER'S TICKETS
        # ----------------------------------------------------

        if intent == "my_tickets":

            if result.get("found") is not True:

                state["verification_result"] = (
                    result.get(
                        "message",
                        "No support tickets found."
                    )
                )

                return state

            tickets = result.get("tickets")

            if tickets is None:

                state["verification_result"] = (
                    "Support ticket list is missing."
                )

                return state

            state["verification_result"] = (
                f"Retrieved {len(tickets)} support ticket(s)."
            )

            return state

    
        # ----------------------------------------------------
        # UPDATE TICKETS
        # ----------------------------------------------------

        if intent == "update_ticket":

            if result.get("success") is not True:

                state["verification_result"] = result.get(
                    "error",
                    result.get(
                        "message",
                        "Support ticket could not be updated."
                    )
                )

                return state

            updated_ticket_id = result.get("ticket_id")
            old_status = result.get("old_status")
            new_status = result.get("new_status")

            if updated_ticket_id is None:
                state["verification_result"] = (
                    "Ticket was updated but ticket ID is missing."
                )
                return state

            if new_status is None:
                state["verification_result"] = (
                    "Ticket was updated but new status is missing."
                )
                return state

            state["verification_result"] = (
                f"Support ticket #{updated_ticket_id} "
                f"status successfully changed from "
                f"{old_status} to {new_status}."
            )

            return state


        
    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    if capability == "rag":

        state["verification_result"] = (
            "Knowledge-based answer generated."
        )

        return state

    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    state["verification_result"] = (
        "Verification completed."
    )

    return state


# ============================================================
# 9. GENERATE FINAL RESPONSE
# ============================================================

def generate_response(state: SupportState) -> SupportState:

    # RAG already generated an answer
    if state.get("answer"):
        return state

    question = state["question"]
    capability = state.get("capability")
    intent = state.get("intent")
    tool_result = state.get("tool_result")
    verification = state.get("verification_result")

    prompt = f"""
You are a professional customer support AI for a food
delivery application.

Answer the customer's question using ONLY the verified
information below.

Customer question:
{question}

Capability:
{capability}

Intent:
{intent}

Verified tool result:
{tool_result}

Verification:
{verification}

Rules:

1. Never invent information.

2. Never claim an order was cancelled unless:
   - success is true
   - and the verified order status is CANCELLED.

3. If cancellation was successful, clearly tell the customer
   that the order was cancelled.

4. If cancellation failed, clearly explain the reason.

5. Never promise a refund unless the payment/refund system
   explicitly confirms one.

6. If a refund has not yet been processed, say that the
   cancellation and refund are separate processes.

7. Never expose internal database, tool, LangGraph, or
   Gemini information.

8. Keep the answer concise and natural.

9. Do not invent order IDs, prices, statuses, or refund
   information.

10. Answer exactly what the customer asked.

For human escalation:

If a support ticket was successfully created:
- Tell the user that a support ticket was created.
- Include the ticket ID.
- Include its status.
- Mention the priority when available.
- Do not claim that a human agent has already responded.
- Do not claim a specific response time unless one is provided by the tool.

SUPPORT TICKET RESPONSES:

For a newly created ticket:
- Tell the user the ticket was created.
- Include the ticket ID.
- Include priority when available.
- Include status when available.
- Do not claim a human has already responded.

For a specific ticket:
- Report the ticket ID.
- Report issue type.
- Report priority.
- Report current status.
- Do not invent updates or response times.

For a list of tickets:
- Summarize the user's tickets.
- Include ticket IDs and statuses.
- Keep the response concise.
- Do not invent ticket information.

Generate only the customer-facing response.
"""
    
    answer = generate_answer(prompt)

    state["answer"] = answer

    return state