from tools.delivery_tools import (
    get_delivery_status
)


# ==========================================================
# TEST DELIVERY TOOL
# ==========================================================

result = get_delivery_status(
    user_id=4
)


print("\n==============================")
print("DELIVERY TOOL RESULT")
print("==============================")

print(result)