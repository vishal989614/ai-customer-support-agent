from database import get_connection


RESTAURANTS = [
    {
        "name": "Spice Garden",
        "cuisine": "North Indian",
        "address": "Sector 15, Chandigarh",
        "latitude": 30.7415,
        "longitude": 76.7681,
        "rating": 4.5,
        "is_open": True,
    },
    {
        "name": "Delhi Zaika",
        "cuisine": "North Indian",
        "address": "Model Town, Delhi",
        "latitude": 28.7031,
        "longitude": 77.1898,
        "rating": 4.3,
        "is_open": True,
    },
    {
        "name": "South Indian House",
        "cuisine": "South Indian",
        "address": "Sector 22, Chandigarh",
        "latitude": 30.7333,
        "longitude": 76.7794,
        "rating": 4.4,
        "is_open": True,
    },
    {
        "name": "Pizza Hub",
        "cuisine": "Italian",
        "address": "Civil Lines, Delhi",
        "latitude": 28.6810,
        "longitude": 77.2220,
        "rating": 4.2,
        "is_open": True,
    },
    {
        "name": "Burger Point",
        "cuisine": "Fast Food",
        "address": "Sector 17, Chandigarh",
        "latitude": 30.7410,
        "longitude": 76.7936,
        "rating": 4.1,
        "is_open": True,
    },
]


DISHES = [
    # Spice Garden
    {
        "restaurant": "Spice Garden",
        "name": "Paneer Tikka",
        "description": "Grilled Indian cottage cheese with spices",
        "category": "Starter",
        "price": 220.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Spice Garden",
        "name": "Butter Chicken",
        "description": "Creamy tomato-based chicken curry",
        "category": "Main Course",
        "price": 320.00,
        "is_vegetarian": False,
        "is_available": True,
    },
    {
        "restaurant": "Spice Garden",
        "name": "Veg Biryani",
        "description": "Aromatic basmati rice cooked with vegetables",
        "category": "Rice",
        "price": 240.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Spice Garden",
        "name": "Dal Makhani",
        "description": "Slow-cooked black lentils with butter and cream",
        "category": "Main Course",
        "price": 190.00,
        "is_vegetarian": True,
        "is_available": True,
    },

    # Delhi Zaika
    {
        "restaurant": "Delhi Zaika",
        "name": "Chole Bhature",
        "description": "Spicy chickpeas served with fluffy bhature",
        "category": "Main Course",
        "price": 160.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Delhi Zaika",
        "name": "Butter Naan",
        "description": "Soft Indian bread topped with butter",
        "category": "Bread",
        "price": 60.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Delhi Zaika",
        "name": "Chicken Tikka",
        "description": "Char-grilled marinated chicken",
        "category": "Starter",
        "price": 280.00,
        "is_vegetarian": False,
        "is_available": True,
    },

    # South Indian House
    {
        "restaurant": "South Indian House",
        "name": "Masala Dosa",
        "description": "Crispy dosa filled with spiced potato",
        "category": "South Indian",
        "price": 130.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "South Indian House",
        "name": "Idli Sambar",
        "description": "Soft steamed idlis served with sambar",
        "category": "South Indian",
        "price": 100.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "South Indian House",
        "name": "Paneer Dosa",
        "description": "Crispy dosa filled with spiced paneer",
        "category": "South Indian",
        "price": 170.00,
        "is_vegetarian": True,
        "is_available": True,
    },

    # Pizza Hub
    {
        "restaurant": "Pizza Hub",
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato, mozzarella and basil",
        "category": "Pizza",
        "price": 250.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Pizza Hub",
        "name": "Farmhouse Pizza",
        "description": "Pizza topped with fresh vegetables",
        "category": "Pizza",
        "price": 320.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Pizza Hub",
        "name": "Chicken Pepperoni Pizza",
        "description": "Pizza topped with chicken pepperoni and cheese",
        "category": "Pizza",
        "price": 380.00,
        "is_vegetarian": False,
        "is_available": True,
    },

    # Burger Point
    {
        "restaurant": "Burger Point",
        "name": "Veg Burger",
        "description": "Crispy vegetable patty with fresh vegetables",
        "category": "Burger",
        "price": 140.00,
        "is_vegetarian": True,
        "is_available": True,
    },
    {
        "restaurant": "Burger Point",
        "name": "Chicken Burger",
        "description": "Grilled chicken patty with lettuce and sauce",
        "category": "Burger",
        "price": 190.00,
        "is_vegetarian": False,
        "is_available": True,
    },
    {
        "restaurant": "Burger Point",
        "name": "French Fries",
        "description": "Crispy golden potato fries",
        "category": "Sides",
        "price": 90.00,
        "is_vegetarian": True,
        "is_available": True,
    },
]


def seed_restaurants(cursor):

    restaurant_ids = {}

    restaurant_query = """
        INSERT INTO restaurants
        (
            name,
            cuisine,
            address,
            latitude,
            longitude,
            rating,
            is_open
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
    """

    for restaurant in RESTAURANTS:

        cursor.execute(
            restaurant_query,
            (
                restaurant["name"],
                restaurant["cuisine"],
                restaurant["address"],
                restaurant["latitude"],
                restaurant["longitude"],
                restaurant["rating"],
                restaurant["is_open"],
            )
        )

        restaurant_ids[
            restaurant["name"]
        ] = cursor.lastrowid

    return restaurant_ids


def seed_dishes(cursor, restaurant_ids):

    dish_query = """
        INSERT INTO dishes
        (
            restaurant_id,
            name,
            description,
            category,
            price,
            is_vegetarian,
            is_available
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
    """

    for dish in DISHES:

        restaurant_id = restaurant_ids[
            dish["restaurant"]
        ]

        cursor.execute(
            dish_query,
            (
                restaurant_id,
                dish["name"],
                dish["description"],
                dish["category"],
                dish["price"],
                dish["is_vegetarian"],
                dish["is_available"],
            )
        )


def main():

    connection = get_connection()

    cursor = connection.cursor()

    try:

        print("Seeding restaurants...")

        restaurant_ids = seed_restaurants(
            cursor
        )

        print(
            f"Inserted {len(restaurant_ids)} restaurants."
        )

        print("Seeding dishes...")

        seed_dishes(
            cursor,
            restaurant_ids
        )

        print(
            f"Inserted {len(DISHES)} dishes."
        )

        connection.commit()

        print("\nDatabase seeding completed.")

    except Exception as e:

        connection.rollback()

        print("\nSeeding failed.")
        print("Error:", e)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()