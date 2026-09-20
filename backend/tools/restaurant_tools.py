from services.restaurant_service import (
    get_restaurant_information as fetch_restaurant_information,
    find_restaurant_by_name
)


def get_restaurant_information(
    restaurant_id: int
):

    if restaurant_id is None:

        return {
            "found": False,
            "error": "Restaurant ID is required."
        }

    return fetch_restaurant_information(
        restaurant_id
    )

def get_restaurant_by_name(
    restaurant_name: str
):

    if not restaurant_name:

        return {
            "found": False,
            "error": "Restaurant name is required."
        }

    result = find_restaurant_by_name(
        restaurant_name
    )

    if not result["found"]:

        return result

    restaurant_id = result[
        "restaurant"
    ]["id"]

    return fetch_restaurant_information(
        restaurant_id
    )