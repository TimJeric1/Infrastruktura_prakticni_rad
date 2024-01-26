from flask import Flask, jsonify
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


# API endpoint to read data from the 'cart' table
@app.route("/api/read-cart")
def read_cart():
    query = "SELECT * FROM cart"
    return jsonify(execute_select_query(query))


# API endpoint to read data from the 'categories' table
@app.route("/api/read-categories")
def read_categories():
    query = "SELECT * FROM categories"
    return jsonify(execute_select_query(query))


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


@app.route("/api/")
def hello():
    return "Flaskapp Master here"


if __name__ == "__main__":
    app.run(debug=True)
