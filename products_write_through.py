from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create Postgres connection object
'''
connection = MySqlConnection('mydb_user', 'mydb_pwd', 'mysql_master:3306/mydb')

'''
Create Postgres users connector
'''

productConnector = MySqlConnector(connection, 'products', 'product_id')

product_mapping = {
    'name': 'name',
    'description': 'description',
    'price': 'price',
    'category_id': 'category_id'
}





RGWriteThrough(GB, keysPrefix='___', mappings=product_mapping,
               connector=productConnector, name='ProductWriteThrough', version='99.99.99')
