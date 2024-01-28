from faker import Faker
import mysql.connector
import redis

fake = Faker()

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost", port=3306, user="root", password="111", database="mydb"
)

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

mycursor = mydb.cursor()

# Drop tables if they exist
mycursor.execute("DROP TABLE IF EXISTS order_items")
mycursor.execute("DROP TABLE IF EXISTS orders")
mycursor.execute("DROP TABLE IF EXISTS users")
mycursor.execute("DROP TABLE IF EXISTS products")

# Create "products" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS products (product_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, price DECIMAL(10, 2));"
)

# Create "users" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), password VARCHAR(255));"
)

# Create "orders" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS orders (order_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, date_ordered DATE, status VARCHAR(50), cost DECIMAL(10, 2), FOREIGN KEY (user_id) REFERENCES users(user_id));"
)

# Create "order_items" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS order_items (order_item_id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_id INT, quantity INT, price DECIMAL(10, 2), FOREIGN KEY (order_id) REFERENCES orders(order_id), FOREIGN KEY (product_id) REFERENCES products(product_id));"
)

print("Inserting data into tables and Redis...")

# Insert data into "products" table and store in Redis
for i in range(1000):
    name = fake.word()
    description = fake.text()
    price = fake.random.uniform(10, 1000)

    #sql = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
    #val = (name, description, price)
    #mycursor.execute(sql, val)

    # Store product data in Redis
    product_key = f"product:{i}"
    product_mapping = {
        'name': name,
        'description': description,
        'price': price
    }
    redis_client.hset(product_key, mapping=product_mapping)

# Insert a specific user into the "users" table
name = "duje"
email = "dujevidas123@gmail.com"
password = "DVidas123"

#sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
#val = (name, email, password)
#mycursor.execute(sql, val)

# Store specific user data in Redis
user_index = 1
user_key = f"user:{user_index}"
user_mapping = {'name': name, 'email': email, 'password': password}
redis_client.hset(user_key, mapping=user_mapping)

# Insert data into "users" table and store in Redis
for i in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()

    #sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    #val = (name, email, password)
    #mycursor.execute(sql, val)

    # Store user data in Redis
    #user_id = mycursor.lastrowid
    user_key = f"user:{i}"
    user_mapping = {'name': name, 'email': email, 'password': password}
    redis_client.hset(user_key, mapping=user_mapping)

mydb.commit()
mycursor.close()
mydb.close()
print("Data inserted into tables and Redis.")
