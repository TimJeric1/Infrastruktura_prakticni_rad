from rgsync import RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create Postgres connection object
'''
connection = MySqlConnection('mydb_user', 'mydb_pwd', 'mysql_master:3306/mydb')

'''
Create Postgres users connector
'''
usersConnector = MySqlConnector(connection, 'users', 'user_id')

user_mapping = {'name': 'name', 'email': 'email', 'password': 'password'}




RGWriteThrough(GB, keysPrefix='_', mappings=user_mapping,
               connector=usersConnector, name='UserWriteThrough', version='99.99.99')
