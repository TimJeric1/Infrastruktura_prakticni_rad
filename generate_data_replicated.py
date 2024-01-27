from faker import Faker
import mysql.connector
from datetime import datetime

fake = Faker()

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="111",
    database="mydb"
)

mycursor = mydb.cursor()

# Create "products" table
mycursor.execute("CREATE TABLE IF NOT EXISTS products (product_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, price DECIMAL(10, 2));")



# Create "users" table
mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), password VARCHAR(255));")

# Create "orders" table
mycursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, date_ordered DATE, status VARCHAR(50), FOREIGN KEY (user_id) REFERENCES users(user_id));")

# Create "order_items" table
mycursor.execute("CREATE TABLE IF NOT EXISTS order_items (order_item_id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_id INT, quantity INT, price DECIMAL(10, 2), FOREIGN KEY (order_id) REFERENCES orders(order_id), FOREIGN KEY (product_id) REFERENCES products(product_id));")

print("Inserting data into tables...")



# Insert data into "products" table
for _ in range(1000):
    name = fake.word()
    description = fake.text()
    price = fake.random.uniform(10, 1000)

    sql = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    val = (name, description, price)
    mycursor.execute(sql, val)

# Insert a specific user into the "users" table
name = "duje"
email = "dujevidas123@gmail.com"
password = "DVidas123"

sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
val = (name, email, password)
mycursor.execute(sql, val)

# Insert data into "users" table
for _ in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    mycursor.execute(sql, val)

# Insert data into "orders" and "order_items" tables
"""
for _ in range(500):
    user_id = fake.random_int(1, 100)  # Assuming you have 100 users
    date_ordered = fake.date_between(start_date='-30d', end_date='today')  # Orders within the last 30 days
    status = fake.random_element(elements=('Processing', 'Shipped', 'Delivered'))
    sql = "INSERT INTO orders (user_id, date_ordered, status) VALUES (%s, %s, %s)"
    val = (user_id, date_ordered, status)
    mycursor.execute(sql, val)

    order_id = mycursor.lastrowid  # Get the last inserted order_id

    for _ in range(fake.random_int(1, 5)):  # Random number of items per order (1 to 5)
        product_id = fake.random_int(1, 1000)  # Assuming you have 1000 products
        quantity = fake.random_int(1, 10)
        price = fake.random.uniform(10, 1000)
        sql = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
        val = (order_id, product_id, quantity, price)
        mycursor.execute(sql, val)
"""
mydb.commit()
mycursor.close()
mydb.close()
print("Data inserted into tables.")
