from tools.restaurant_tools import (
    get_restaurant_information
)


result = get_restaurant_information(
    restaurant_id=100
)


print("\n==============================")
print("RESTAURANT TOOL RESULT")
print("==============================")

print(result)