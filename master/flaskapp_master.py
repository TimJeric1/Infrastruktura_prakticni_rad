from flask import Flask, jsonify, request
import mysql.connector.pooling
import time

app = Flask(__name__)


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



# API endpoint to read data from the 'orders' table
@app.route("/api/read-orders")
def read_orders():
    query = "SELECT * FROM orders"
    return jsonify(execute_select_query(query))


# API endpoint to read data from the 'products' table
@app.route("/api/read-products")
def read_products():
    query = "SELECT * FROM products"
    return jsonify(execute_select_query(query))


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
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
        result = execute_select_query(query)

        if result:
            # Assuming 'result' is a dictionary containing user information
            user_info = result[0]  # Assuming there's only one user with the given email and password
            return jsonify({"status": "success", "message": "Login successful", "user": user_info})
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
            return jsonify({"status": "error", "message": "User with this email already exists"})

        # Insert the new user into the 'users' table
        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        insert_values = (name, email, password)
        execute_query(insert_query, insert_values)

        # Retrieve the newly registered user
        user_query = f"SELECT * FROM users WHERE email = '{email}'"
        new_user = execute_select_query(user_query)

        return jsonify({"status": "success", "message": "User registered successfully", "user": new_user[0]})
    else:
        return jsonify({"status": "error", "message": "Invalid request"})


if __name__ == "__main__":
    app.run(debug=True)
