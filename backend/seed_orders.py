from database import get_connection


def get_restaurant_id(cursor, restaurant_name):

    cursor.execute(
        """
        SELECT id
        FROM restaurants
        WHERE name = %s
        """,
        (restaurant_name,)
    )

    result = cursor.fetchone()

    if not result:
        raise ValueError(
            f"Restaurant not found: {restaurant_name}"
        )

    return result["id"]


def get_dish(cursor, restaurant_id, dish_name):

    cursor.execute(
        """
        SELECT id, price
        FROM dishes
        WHERE restaurant_id = %s
        AND name = %s
        """,
        (restaurant_id, dish_name)
    )

    result = cursor.fetchone()

    if not result:
        raise ValueError(
            f"Dish not found: {dish_name}"
        )

    return result


def create_users(cursor):

    users = [
        (
            "Rahul Sharma",
            "rahul@example.com",
            "9876543210"
        ),
        (
            "Aman Verma",
            "aman@example.com",
            "9876543211"
        ),
        (
            "Priya Singh",
            "priya@example.com",
            "9876543212"
        ),
    ]

    query = """
        INSERT INTO users
        (
            name,
            email,
            phone
        )
        VALUES
        (
            %s, %s, %s
        )
    """

    user_ids = {}

    for user in users:

        cursor.execute(query, user)

        user_ids[user[0]] = cursor.lastrowid

    return user_ids


def create_order(
    cursor,
    user_id,
    restaurant_id,
    status,
    total_amount,
    address
):

    query = """
        INSERT INTO orders
        (
            user_id,
            restaurant_id,
            status,
            total_amount,
            delivery_address
        )
        VALUES
        (
            %s, %s, %s, %s, %s
        )
    """

    cursor.execute(
        query,
        (
            user_id,
            restaurant_id,
            status,
            total_amount,
            address
        )
    )

    return cursor.lastrowid


def create_order_item(
    cursor,
    order_id,
    dish_id,
    quantity,
    price
):

    query = """
        INSERT INTO order_items
        (
            order_id,
            dish_id,
            quantity,
            price
        )
        VALUES
        (
            %s, %s, %s, %s
        )
    """

    cursor.execute(
        query,
        (
            order_id,
            dish_id,
            quantity,
            price
        )
    )


def create_delivery(
    cursor,
    order_id,
    partner_name,
    partner_phone,
    status
):

    query = """
        INSERT INTO deliveries
        (
            order_id,
            delivery_partner_name,
            delivery_partner_phone,
            status,
            estimated_delivery_time
        )
        VALUES
        (
            %s, %s, %s, %s,
            DATE_ADD(NOW(), INTERVAL 25 MINUTE)
        )
    """

    cursor.execute(
        query,
        (
            order_id,
            partner_name,
            partner_phone,
            status
        )
    )


def create_payment(
    cursor,
    order_id,
    amount,
    payment_method,
    status,
    transaction_id
):

    query = """
        INSERT INTO payments
        (
            order_id,
            amount,
            payment_method,
            status,
            transaction_id
        )
        VALUES
        (
            %s, %s, %s, %s, %s
        )
    """

    cursor.execute(
        query,
        (
            order_id,
            amount,
            payment_method,
            status,
            transaction_id
        )
    )


def main():

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        print("Creating users...")

        user_ids = create_users(cursor)

        print(
            f"Created {len(user_ids)} users."
        )

        # --------------------------------
        # Get actual restaurant IDs
        # --------------------------------

        spice_garden_id = get_restaurant_id(
            cursor,
            "Spice Garden"
        )

        delhi_zaika_id = get_restaurant_id(
            cursor,
            "Delhi Zaika"
        )

        south_indian_id = get_restaurant_id(
            cursor,
            "South Indian House"
        )

        # --------------------------------
        # Get actual dish information
        # --------------------------------

        paneer_tikka = get_dish(
            cursor,
            spice_garden_id,
            "Paneer Tikka"
        )

        butter_chicken = get_dish(
            cursor,
            spice_garden_id,
            "Butter Chicken"
        )

        masala_dosa = get_dish(
            cursor,
            south_indian_id,
            "Masala Dosa"
        )

        chole_bhature = get_dish(
            cursor,
            delhi_zaika_id,
            "Chole Bhature"
        )

        # =================================
        # ORDER 1
        # Rahul - OUT FOR DELIVERY
        # =================================

        order_1 = create_order(
            cursor,
            user_ids["Rahul Sharma"],
            spice_garden_id,
            "OUT_FOR_DELIVERY",
            540.00,
            "Sector 15, Chandigarh"
        )

        create_order_item(
            cursor,
            order_1,
            paneer_tikka["id"],
            1,
            paneer_tikka["price"]
        )

        create_order_item(
            cursor,
            order_1,
            butter_chicken["id"],
            1,
            butter_chicken["price"]
        )

        create_delivery(
            cursor,
            order_1,
            "Rohit Kumar",
            "9876500000",
            "ON_THE_WAY"
        )

        create_payment(
            cursor,
            order_1,
            540.00,
            "UPI",
            "SUCCESS",
            "TXN_RAHUL_001"
        )

        # =================================
        # ORDER 2
        # Aman - PREPARING
        # =================================

        order_2 = create_order(
            cursor,
            user_ids["Aman Verma"],
            south_indian_id,
            "PREPARING",
            260.00,
            "Sector 22, Chandigarh"
        )

        create_order_item(
            cursor,
            order_2,
            masala_dosa["id"],
            2,
            masala_dosa["price"]
        )

        create_payment(
            cursor,
            order_2,
            260.00,
            "CARD",
            "SUCCESS",
            "TXN_AMAN_001"
        )

        # =================================
        # ORDER 3
        # Priya - DELIVERED
        # =================================

        order_3 = create_order(
            cursor,
            user_ids["Priya Singh"],
            delhi_zaika_id,
            "DELIVERED",
            160.00,
            "Model Town, Delhi"
        )

        create_order_item(
            cursor,
            order_3,
            chole_bhature["id"],
            1,
            chole_bhature["price"]
        )

        create_delivery(
            cursor,
            order_3,
            "Suresh Kumar",
            "9876500001",
            "DELIVERED"
        )

        create_payment(
            cursor,
            order_3,
            160.00,
            "UPI",
            "SUCCESS",
            "TXN_PRIYA_001"
        )

        connection.commit()

        print("\nOrder test data created successfully.")

        print(f"Order 1: {order_1}")
        print(f"Order 2: {order_2}")
        print(f"Order 3: {order_3}")

    except Exception as e:

        connection.rollback()

        print("\nSeeding failed.")
        print("Error:", e)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()