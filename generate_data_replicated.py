import mysql.connector
from faker import Faker
import redis

fake = Faker()
# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="111",
    database="mydb"
)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

mycursor = mydb.cursor()

# Create "products" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS products (product_id SERIAL PRIMARY KEY, name VARCHAR(255), description TEXT, price DECIMAL(10, 2), category_id INT);")

# Create "categories" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS categories (category_id SERIAL PRIMARY KEY, name VARCHAR(255));")

# Create "users" table (if not exists)
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), password VARCHAR(255));")
# Create "cart" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS cart (cart_id SERIAL PRIMARY KEY, user_id BIGINT UNSIGNED NOT NULL UNIQUE, product_id BIGINT UNSIGNED NOT NULL UNIQUE, quantity INT, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (product_id) REFERENCES products(product_id));")

# Create "orders" table
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS orders (order_id SERIAL PRIMARY KEY, user_id BIGINT UNSIGNED NOT NULL UNIQUE, date_ordered DATE, status VARCHAR(50), FOREIGN KEY (user_id) REFERENCES users(user_id));")

print("Inserting data into tables...")
# Insert data into "products" hash and keep track of product keys in a set
for i in range(1000):
    name = fake.word()
    description = fake.text()
    price = fake.random.uniform(10, 1000)
    category_id = fake.random_int(1, 10)

    product_key = f"product:{i}"
    product_mapping = {
        'name': name,
        'description': description,
        'price': price,
        'category_id': category_id
    }
    redis_client.hset(f"___{{{product_key}}}", mapping=product_mapping)
    redis_client.sadd('products', product_key)

# Insert data into "categories" hash and keep track of category keys in a set
for i in range(10):
    category_name = fake.word()
    category_key = f"category:{i}"
    category_mapping = {'name': category_name}
    redis_client.hset(f"__{{{category_key}}}", mapping=category_mapping)
    redis_client.sadd('categories', category_key)

# Insert data into "users" hash and keep track of user keys in a set
for i in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()

    user_key = f"user:{i}"
    user_mapping = {'name': name, 'email': email, 'password': password}
    redis_client.hset(f"_{{{user_key}}}", mapping=user_mapping)
    redis_client.sadd('users', user_key)

mydb.commit()
mycursor.close()
mydb.close()
print("Data inserted into tables.")
