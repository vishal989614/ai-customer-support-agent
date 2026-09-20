from database import get_connection


def get_restaurant_by_id(
    restaurant_id: int
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            id,
            name,
            cuisine,
            address,
            latitude,
            longitude,
            rating,
            is_open,
            created_at
        FROM restaurants
        WHERE id = %s
    """

    try:

        cursor.execute(
            query,
            (restaurant_id,)
        )

        restaurant = cursor.fetchone()

        if not restaurant:

            return {
                "found": False,
                "message": "Restaurant not found."
            }

        return {
            "found": True,
            "restaurant": restaurant
        }

    finally:

        cursor.close()
        connection.close()


def get_restaurant_dishes(
    restaurant_id: int
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            id,
            name,
            description,
            category,
            price,
            is_vegetarian,
            is_available
        FROM dishes
        WHERE restaurant_id = %s
        ORDER BY id
    """

    try:

        cursor.execute(
            query,
            (restaurant_id,)
        )

        dishes = cursor.fetchall()

        return dishes

    finally:

        cursor.close()
        connection.close()


def get_restaurant_information(
    restaurant_id: int
):

    restaurant_result = get_restaurant_by_id(
        restaurant_id
    )

    if not restaurant_result["found"]:

        return restaurant_result

    restaurant = restaurant_result[
        "restaurant"
    ]

    dishes = get_restaurant_dishes(
        restaurant_id
    )

    return {
        "found": True,

        "restaurant": restaurant,

        "dishes": dishes
    }

def find_restaurant_by_name(
    restaurant_name: str
):

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
        SELECT
            id,
            name,
            cuisine,
            address,
            latitude,
            longitude,
            rating,
            is_open
        FROM restaurants
        WHERE LOWER(name) = LOWER(%s)
        LIMIT 1
    """

    try:

        cursor.execute(
            query,
            (restaurant_name,)
        )

        restaurant = cursor.fetchone()

        if not restaurant:

            return {
                "found": False,
                "message": "Restaurant not found."
            }

        return {
            "found": True,
            "restaurant": restaurant
        }

    finally:

        cursor.close()
        connection.close()