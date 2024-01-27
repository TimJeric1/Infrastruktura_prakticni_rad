from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create Postgres connection object
'''
connection = MySqlConnection('mydb_user', 'mydb_pwd', 'mysql_master:3306/mydb')

'''
Create Postgres users connector
'''
categoryConnector = MySqlConnector(connection, 'categories', 'category_id')


category_mapping = {'name': 'name'}





RGWriteThrough(GB, keysPrefix='__', mappings=category_mapping,
               connector=categoryConnector, name='CategoryWriteThrough', version='99.99.99')
