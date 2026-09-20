from tools.support_tools import escalate_to_human


result = escalate_to_human(
    user_id=4,
    order_id=2,
    issue_type="GENERAL_SUPPORT",
    description="I need help with my order.",
    priority="MEDIUM"
)

print("\nSupport Ticket Result:")
print(result)