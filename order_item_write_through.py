from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create Postgres connection object
'''
connection = MySqlConnection('mydb_user', 'mydb_pwd', 'mysql_master:3306/mydb')

'''
Create Postgres users connector
'''
# Create MySQL order_items connector
orderItemsConnector = MySqlConnector(connection, 'order_items', 'order_item_id')

# Mapping for the 'order_items' table
order_items_mapping = {'order_id': 'order_id', 'product_id': 'product_id', 'quantity': 'quantity', 'price': 'price'}

# RGWriteThrough block for 'order_items'
RGWriteThrough(GB, keysPrefix='____', mappings=order_items_mapping,
               connector=orderItemsConnector, name='OrderItemsWriteThrough', version='99.99.99')


