from tools.support_tools import update_ticket_status


result = update_ticket_status(
    user_id=4,
    ticket_id=7,
    new_status="IN_PROGRESS"
)

print("\nResult:")
print(result)