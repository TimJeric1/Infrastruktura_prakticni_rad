from flask import Flask, jsonify
import redis
import time

app = Flask(__name__)

def create_redis_connection():
    try:
        return redis.Redis(host="redis", port=6379, decode_responses=True)
    except redis.RedisError as err:
        print(f"Error connecting to Redis: {err}")
        time.sleep(1)

# Create a new Redis connection for each request
redis_connection = create_redis_connection()

# Helper function to execute a Redis HGETALL command and return results as JSON
def execute_hgetall_command(key):
    try:
        values = []
        keys = redis_connection.smembers(name=key)
        for key in keys:
            values.append(redis_connection.hgetall(key))
        return values
    except redis.RedisError as err:
        return {"error": f"Redis Error: {err}"}

# API endpoint to read data from the 'cart' table
@app.route("/api/read-cart")
def read_cart():
    key = "carts"  # Assuming 'cart' is a Redis hash key
    return jsonify(execute_hgetall_command(key))

# API endpoint to read data from the 'categories' table
@app.route("/api/read-categories")
def read_categories():
    key = "categories"  # Assuming 'categories' is a Redis hash key
    return jsonify(execute_hgetall_command(key))

# API endpoint to read data from the 'orders' table
@app.route("/api/read-orders")
def read_orders():
    key = "orders"  # Assuming 'orders' is a Redis hash key
    return jsonify(execute_hgetall_command(key))

# API endpoint to read data from the 'products' table
@app.route("/api/read-products")
def read_products():
    key = "products"  # Assuming 'products' is a Redis hash key
    return jsonify(execute_hgetall_command(key))

# API endpoint to read data from the 'users' table
@app.route("/api/read-users")
def read_users():
    key = "users"  # Assuming 'users' is a Redis hash key
    return jsonify(execute_hgetall_command(key))

@app.route("/api/")
def hello():
    return "Flaskapp Master here"


if __name__ == "__main__":
    app.run(debug=True)
