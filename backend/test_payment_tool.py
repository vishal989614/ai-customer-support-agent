from tools.payment_tools import get_payment_status


result = get_payment_status(
    user_id=4
)


print("\n==============================")
print("PAYMENT TOOL RESULT")
print("==============================")

print(result)