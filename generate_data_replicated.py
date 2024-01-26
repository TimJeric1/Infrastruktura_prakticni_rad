from faker import Faker
import mysql.connector

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
mycursor.execute("CREATE TABLE IF NOT EXISTS products (product_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, price DECIMAL(10, 2), category_id INT);")

# Create "categories" table
mycursor.execute("CREATE TABLE IF NOT EXISTS categories (category_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));")

# Create "users" table (if not exists)
mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), password VARCHAR(255));")

# Create "cart" table
mycursor.execute("CREATE TABLE IF NOT EXISTS cart (cart_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, product_id INT, quantity INT, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (product_id) REFERENCES products(product_id));")

# Create "orders" table
mycursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, date_ordered DATE, status VARCHAR(50), FOREIGN KEY (user_id) REFERENCES users(user_id));")

print("Inserting data into tables...")

# Insert data into "products" and "categories" tables
for _ in range(1000):
    name = fake.word()
    description = fake.text()
    price = fake.random.uniform(10, 1000)
    category_id = fake.random_int(1, 10)  # Assuming you have 10 categories
    sql = "INSERT INTO products (name, description, price, category_id) VALUES (%s, %s, %s, %s)"
    val = (name, description, price, category_id)
    mycursor.execute(sql, val)

for _ in range(10):
    category_name = fake.word()
    sql = "INSERT INTO categories (name) VALUES (%s)"
    val = (category_name,)
    mycursor.execute(sql, val)

# Insert data into "users" table
for _ in range(100):
    name = fake.name()
    email = fake.email()
    password = fake.password()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    mycursor.execute(sql, val)

mydb.commit()
mycursor.close()
mydb.close()
print("Data inserted into tables.")
