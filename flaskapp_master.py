from flask import Flask, jsonify
import mysql.connector.pooling
import time

app = Flask(__name__)

# Initialize connection pool configurations for both ports
dbconfig_master = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "111",
    "database": "mydb"
}

# Create connection pools for both ports
master_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="master_pool", pool_size=5, **dbconfig_master)

# Create iterators for the connection pools
pool_cycle = iter([master_pool])


# Function to get a connection from the pools with round-robin load balancing
def get_connection():
    global pool_cycle  # Declare pool_cycle as global

    while True:
        try:
            # Get the next available connection pool in a round-robin manner
            pool = next(pool_cycle)
            return pool.get_connection()

        except StopIteration:  # Reset the iterator if exhausted
            pool_cycle = iter([master_pool])
            print("Connection pools exhausted, resetting the iterator.")
            time.sleep(1)


# Route that performs a database read operation
@app.route('/read-users')
def read_users():
    try:
        # Attempt to get a connection from the pools with round-robin load balancing
        cnx = get_connection()

        cursor = cnx.cursor()

        # Execute your read query (replace 'your_table' and 'your_column' with appropriate names)
        query = "SELECT * FROM users"
        cursor.execute(query)

        # PROCESSING
        time.sleep(0.5)

        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return jsonify(data)

    except mysql.connector.Error as err:
        return f"Error: {err}\n"


if __name__ == '__main__':
    app.run(debug=True)
