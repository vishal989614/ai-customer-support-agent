import mysql.connector
from mysql.connector import pooling
from config import settings

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="support_pool",
                pool_size=10,
                pool_reset_session=True,
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE
            )
        except Exception:
            _pool = None
    return _pool

def get_connection():
    pool = get_pool()
    if pool is not None:
        try:
            return pool.get_connection()
        except Exception:
            pass
    # Fallback to direct connection
    return mysql.connector.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE
    )