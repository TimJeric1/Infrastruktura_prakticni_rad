from faker import Faker
import pymysql
import redis

fake = Faker()

# Connect to MySQL
mydb = pymysql.connect(
    host="localhost", port=3306, user="root", password="111", database="mydb"
)

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

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
redis_client.delete("products", "orders", "users", "order_items")

# Insert data into "products" table and store in Redis
for i in range(1000):
    name = fake.word()
    description = fake.text()
    price = fake.random.uniform(10, 1000)

    product_key = f"product:{i}"
    product_mapping = {
        "name": name,
        "description": description,
        "price": price,
    }
    redis_client.hset(f"_{{{product_key}}}", mapping=product_mapping)
    redis_client.sadd("products", product_key)



# Insert data into "orders" table and store in Redis
for i in range(5):
    user_id = fake.random_int(1, 5)  # Make sure user_id exists in the users table
    date_ordered = fake.date()
    status = fake.random_element(elements=("pending", "shipped", "delivered"))
    cost = fake.random.uniform(10, 1000)

    order_key = f"order:{i}"
    order_mapping = {
        "user_id": user_id,
        "date_ordered": date_ordered,
        "status": status,
        "cost": cost,
    }
    print(f"Inserting order {i}: {order_mapping}")
    redis_client.hset(f"_{{{order_key}}}", mapping=order_mapping)
    redis_client.sadd("orders", order_key)

# Insert data into "users" table and store in Redis
for i in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()

    user_key = f"user:{i}"
    user_mapping = {"name": name, "email": email, "password": password}
    redis_client.hset(f"_{{{user_key}}}", mapping=user_mapping)
    redis_client.sadd("users", user_key)

order_keys = sorted(redis_client.smembers("orders"))

# Print the details for each order
print("Order details:")
for order_key in order_keys:
    order_data = redis_client.hgetall(order_key)
    print(f"Order Key: {order_key}, Order Data: {order_data}")
mydb.commit()
mycursor.close()
mydb.close()
print("Data inserted into tables and Redis.")
