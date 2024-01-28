from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create MySql connection object
'''
connection = MySqlConnection('mydb_user', 'mydb_pwd', 'mysql_master:3306/mydb')

'''
Create MySql users connector
'''

productConnector = MySqlConnector(connection, 'products', 'product_id')

product_mapping = {
    'name': 'name',
    'description': 'description',
    'price': 'price',
}


RGWriteThrough(GB, keysPrefix='_', mappings=product_mapping,
               connector=productConnector, name='ProductWriteThrough', version='99.99.99')