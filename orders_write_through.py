from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

"""
Create Postgres connection object
"""
connection = MySqlConnection("mydb_user", "mydb_pwd", "mysql_master:3306/mydb")

"""
Create Postgres users connector
"""

ordersConnector = MySqlConnector(connection, "orders", "order_id")

orders_mapping = {
    "user_id": "user_id",
    "date_ordered": "date_ordered",
    "status": "status",
    "cost": "cost",
}

RGWriteThrough(
    GB,
    keysPrefix="_",
    mappings=orders_mapping,
    connector=ordersConnector,
    name="OrdersWriteThrough",
    version="99.99.99",
)
