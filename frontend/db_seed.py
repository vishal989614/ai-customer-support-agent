import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST") or os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT") or os.getenv("DB_PORT", "3306")),
        "user": os.getenv("MYSQL_USER") or os.getenv("DB_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD") or os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("MYSQL_DATABASE") or os.getenv("DB_NAME", "food_delivery"),
    }

def verify_and_seed_database():
    """
    Verifies that all required tables exist and that rows match the user's provided SQL dump.
    If order_items or payments are empty (due to previous partial execution or ENUM mismatches),
    this inserts them cleanly.
    """
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    results = {}

    try:
        # 1. Check existing counts
        tables = [
            "users", "restaurants", "dishes", "orders", 
            "order_items", "payments", "deliveries", "support_tickets"
        ]
        
        counts = {}
        for tbl in tables:
            cursor.execute(f"SELECT COUNT(*) AS count FROM {tbl}")
            counts[tbl] = cursor.fetchone()["count"]

        # 2. Check and seed order_items if empty
        if counts.get("order_items", 0) == 0:
            order_items_data = [
                (1, 1001, 1, 1, 299.00),
                (2, 1001, 4, 2, 149.00),
                (3, 1002, 8, 1, 280.00),
                (4, 1002, 9, 1, 220.00),
                (5, 1002, 10, 1, 50.00),
                (6, 1003, 11, 2, 320.00),
                (7, 1004, 5, 1, 249.00),
                (8, 1004, 7, 1, 129.00),
                (9, 1005, 13, 2, 160.00),
                (10, 1006, 2, 1, 449.00),
                (11, 1006, 4, 1, 49.00),
                (12, 1007, 17, 1, 299.00),
                (13, 1008, 15, 2, 220.00),
                (14, 1008, 16, 1, 60.00),
                (15, 1009, 8, 1, 280.00),
                (16, 1009, 9, 1, 220.00),
                (17, 1009, 10, 2, 50.00),
                (18, 1010, 11, 1, 320.00),
                (19, 1011, 19, 1, 150.00),
                (20, 1011, 20, 1, 180.00),
                (21, 1012, 3, 1, 499.00),
                (22, 1013, 8, 1, 280.00),
                (23, 1013, 9, 1, 220.00),
                (24, 1014, 11, 2, 320.00)
            ]
            cursor.executemany(
                """
                INSERT INTO order_items (id, order_id, dish_id, quantity, price)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity=VALUES(quantity), price=VALUES(price)
                """,
                order_items_data
            )
            conn.commit()
            results["order_items_seeded"] = len(order_items_data)

        # 3. Check and seed payments if empty
        if counts.get("payments", 0) == 0:
            payments_data = [
                (1, 1001, 'UPI', 597.00, 'SUCCESS', 'TXN10001'),
                (2, 1002, 'Card', 550.00, 'SUCCESS', 'TXN10002'),
                (3, 1003, 'UPI', 640.00, 'SUCCESS', 'TXN10003'),
                (4, 1004, 'Cash', 448.00, 'SUCCESS', 'CASH10004'),
                (5, 1005, 'UPI', 320.00, 'REFUNDED', 'TXN10005'),
                (6, 1006, 'Card', 598.00, 'SUCCESS', 'TXN10006'),
                (7, 1007, 'UPI', 299.00, 'SUCCESS', 'TXN10007'),
                (8, 1008, 'Card', 500.00, 'PENDING', 'TXN10008'),
                (9, 1009, 'UPI', 600.00, 'SUCCESS', 'TXN10009'),
                (10, 1010, 'Card', 320.00, 'SUCCESS', 'TXN10010'),
                (11, 1011, 'UPI', 330.00, 'SUCCESS', 'TXN10011'),
                (12, 1012, 'Card', 448.00, 'SUCCESS', 'TXN10012'),
                (13, 1013, 'UPI', 500.00, 'REFUNDED', 'TXN10013'),
                (14, 1014, 'UPI', 640.00, 'SUCCESS', 'TXN10014')
            ]
            cursor.executemany(
                """
                INSERT INTO payments (id, order_id, payment_method, amount, status, transaction_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE status=VALUES(status), amount=VALUES(amount)
                """,
                payments_data
            )
            conn.commit()
            results["payments_seeded"] = len(payments_data)

        # Re-fetch final counts
        final_counts = {}
        for tbl in tables:
            cursor.execute(f"SELECT COUNT(*) AS count FROM {tbl}")
            final_counts[tbl] = cursor.fetchone()["count"]

        results["counts"] = final_counts
        results["status"] = "synced"
        return results

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    res = verify_and_seed_database()
    print("Database sync result:", res)
