from flask import Flask, jsonify, request
import redis
from datetime import datetime

app = Flask(__name__)

# Create a new Redis connection for each request
redis_connection = redis.Redis(host="redis", port=6379, decode_responses=True)


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


# API endpoint to read data from the 'order_items' table
@app.route("/api/read-order-items")
def read_order_items():
    key = "order_items"  # Assuming 'order_items' is a Redis hash key
    return jsonify(execute_hgetall_command(key))


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
        existing_user_keys = redis_connection.smembers("users")
        user_data = None

        for user_key in existing_user_keys:
            user_data = redis_connection.hgetall(user_key)
            if user_data.get("email") == email and user_data.get("password") == password:
                break

        if user_data and user_data["password"] == password:
            return jsonify(
                {"status": "success", "message": "Login successful", "user": user_data}
            )
        else:
            return jsonify({"status": "error", "message": "Invalid email or password", "user": user_data})
    else:
        return jsonify({"status": "error", "message": "Invalid request"})



# API endpoint for user registration
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name and email and password:
        # Get the count of existing users to generate the next user key
        user_count = redis_connection.scard("users")

        user_key = f"user:{user_count + 1}"
        user_data = redis_connection.hgetall(user_key)

        if not user_data:
            # User does not exist, proceed with registration
            user_data = {"name": name, "email": email, "password": password}
            redis_connection.hset(f"_{{{user_key}}}", mapping=user_data)
            redis_connection.sadd('users', user_key)
            return jsonify(
                {
                    "status": "success",
                    "message": "User registered successfully",
                    "user": user_data,
                }
            )
        else:
            return jsonify(
                {"status": "error", "message": "User with this email already exists"}
            )
    else:
        return jsonify({"status": "error", "message": "Invalid request"})


# API endpoint for creating a new order
@app.route("/api/create-order", methods=["POST"])
def create_order():
    data = request.json
    user_id = data.get("user_id")
    products = data.get("products")  # Assuming it's a list of product IDs and quantities

    if user_id and products:
        try:
            # Assuming 'orders' and 'order_items' are Redis hash keys
            
            order_count = redis_connection.scard("orders")  # Increment order count
            order_key = f"order:{order_count+1}"
            total_cost = sum(product["price"] * product["quantity"] for product in products)

            # Store order data in Redis
            order_data = {
                "user_id": user_id,
                "date_ordered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending",
                "cost": total_cost,
            }
            redis_connection.hset(f"_{order_key}", mapping=order_data)
            redis_connection.sadd('orders', order_key)

            # Insert the order items into the 'order_items' table
            for product in products:
                order_item_count = redis_connection.scard("order_items")  # Increment order count
                order_item_key = f"order_items:{order_item_count+1}"
                product_id = product["product_id"]
                quantity = product["quantity"]
                price = product["price"]

                order_item_data = {
                    "order_id": order_key,
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": price,
                }
                redis_connection.hset(f"_{order_item_key}", mapping=order_item_data)
                redis_connection.sadd('order_items', order_item_key)

            return jsonify({"status": "success", "message": "Order created successfully","key":order_key})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid request"})



if __name__ == "__main__":
    app.run(debug=True)
