from flask import Flask, jsonify, request
import redis
import mysql.connector.pooling
import time

app = Flask(__name__)

# Create a new Redis connection for each request
redis_connection = redis.Redis(host="redis", port=6379, decode_responses=True)


# Helper function to execute a Redis HGETALL command and return results as JSON
def execute_hgetall_command(key):
    try:
        result = []
        keys = redis_connection.smembers(name=key)
        for key in keys:
            values = redis_connection.hgetall(key)
            result.append({"key": key, "values": values})
        return result
    except redis.RedisError as err:
        return {"error": f"Redis Error: {err}"}


def create_connection_pool():
    while True:
        try:
            return mysql.connector.pooling.MySQLConnectionPool(
                pool_name="master_pool", pool_size=5, **dbconfig_master
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            time.sleep(1)


def get_connection_from_pool(pool):
    return pool.get_connection()


dbconfig_master = {
    "host": "mysql_master",
    "port": 3306,
    "user": "root",
    "password": "111",
    "database": "mydb",
}

# Create a new connection pool for each request
connection_pool = create_connection_pool()


# Helper function to execute a SELECT query and return results as JSON
def execute_select_query(query):
    try:
        cnx = get_connection_from_pool(connection_pool)
        cursor = cnx.cursor(dictionary=True)  # Return results as dictionaries
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data
    except mysql.connector.Error as err:
        return {"error": f"Database Error: {err}"}


def execute_query(query, values=None):
    try:
        cnx = get_connection_from_pool(connection_pool)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query, values)
        cnx.commit()
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        raise Exception(f"Database Error: {err}")


@app.route("/api/read-orders")
def read_orders():
    query = "SELECT * FROM orders"
    return jsonify(execute_select_query(query))


# API endpoint to read data from the 'products' table
@app.route("/api/read-products")
def read_products():
    key = "products"  # Assuming 'products' is a Redis hash key
    return jsonify(execute_hgetall_command(key))


# API endpoint to read data from the 'users' table
@app.route("/api/read-users")
def read_users():
    query = "SELECT * FROM users"
    return jsonify(execute_select_query(query))


# API endpoint to read data from the 'order_items' table
@app.route("/api/read-order-items")
def read_order_items():
    query = "SELECT * FROM order_items"
    return jsonify(execute_select_query(query))


@app.route("/api/")
def hello():
    return "Flaskapp Master here"


# API endpoint for user login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email and password:
        query = (
            f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
        )
        result = execute_select_query(query)

        if result:
            # Assuming 'result' is a dictionary containing user information
            user_info = result[
                0
            ]  # Assuming there's only one user with the given email and password
            return jsonify(
                {"status": "success", "message": "Login successful", "user": user_info}
            )
        else:
            return jsonify({"status": "error", "message": "Invalid email or password"})

    return jsonify({"status": "error", "message": "Invalid request"})


# API endpoint for user register
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name and email and password:
        # Check if the user with the given email already exists
        check_query = f"SELECT * FROM users WHERE email = '{email}'"
        existing_user = execute_select_query(check_query)

        if existing_user:
            return jsonify(
                {"status": "error", "message": "User with this email already exists"}
            )

        # Insert the new user into the 'users' table
        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        insert_values = (name, email, password)
        execute_query(insert_query, insert_values)

        # Retrieve the newly registered user
        user_query = f"SELECT * FROM users WHERE email = '{email}'"
        new_user = execute_select_query(user_query)

        return jsonify(
            {
                "status": "success",
                "message": "User registered successfully",
                "user": new_user[0],
            }
        )
    else:
        return jsonify({"status": "error", "message": "Invalid request"})


# API endpoint for creating a new order
@app.route("/api/create-order", methods=["POST"])
def create_order():
    data = request.json
    user_id = data.get("user_id")
    products = data.get(
        "products"
    )  # Assuming it's a list of product IDs and quantities

    if user_id and products:
        try:
            # Insert the new order into the 'orders' table
            order_query = "INSERT INTO orders (user_id, date_ordered, status, cost) VALUES (%s, NOW(), 'pending', %s)"
            total_cost = sum(
                product["price"] * product["quantity"] for product in products
            )
            order_values = (user_id, total_cost)
            execute_query(order_query, order_values)

            # Retrieve the ID of the newly created order
            order_id_query = "SELECT * FROM orders ORDER BY order_id DESC LIMIT 1"
            order_id_result = execute_select_query(order_id_query)
            last_order_id = order_id_result[0]["order_id"]

            # Insert the order items into the 'order_items' table
            for product in products:
                product_id = product["product_id"]
                quantity = product["quantity"]
                price = product["price"]

                order_item_query = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
                order_item_values = (last_order_id, product_id, quantity, price)
                execute_query(order_item_query, order_item_values)

            return jsonify(
                {"status": "success", "message": "Order created successfully"}
            )
        except Exception as e:
            return jsonify(
                {"status": "error", "message": str(e), "my_order_id": last_order_id}
            )

    return jsonify({"status": "error", "message": "Invalid request"})


if __name__ == "__main__":
    app.run(debug=True)
