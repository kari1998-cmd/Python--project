import psycopg2
from psycopg2 import sql
from flask import Flask, request, jsonify

# Define the database connection parameters
def get_connection():
    return psycopg2.connect(
        dbname="realoneinvest",  # Use lowercase to avoid PostgreSQL case-sensitivity issues
        user="karthik1",
        password="Info123tech",
        host="localhost",
        port="5433"  # Ensure PostgreSQL is running on this port
    )

# Function to create the users table
def create_users_table():
    try:
        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        # SQL query to create the users table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            phone_number VARCHAR(15),
            address TEXT
        );
        """
        # Execute the query
        cursor.execute(create_table_query)

        # Commit the changes
        conn.commit()

        print("Table 'users' created successfully.")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while creating the table: {error}")

# Initialize Flask app
app = Flask(__name__)

# API endpoint to store user data
@app.route('/api/signup', methods=['POST'])
def store_user():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Extract user details
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        reenter_password = data.get('reenter_password')
        phone_number = data.get('phone_number')
        address = data.get('address')

        # Validate required fields
        if not (first_name and last_name and email and password and reenter_password):
            return jsonify({"error": "First name, last name, email, password, and reentered password are required."}), 400

        # Check if passwords match
        if password != reenter_password:
            return jsonify({"error": "Passwords do not match."}), 400

        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Insert user data into the database
        insert_query = """
        INSERT INTO users (first_name, last_name, email, password, phone_number, address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (first_name, last_name, email, password, phone_number, address))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({"message": "User stored successfully."}), 201

    except (Exception, psycopg2.Error) as error:
        print(f"Error while storing user data: {error}")
        return jsonify({"error": "Failed to store user data."}), 500

# Run the Flask app
if __name__ == '__main__':
    # Create the users table before running the app
    create_users_table()
    app.run(debug=True, host="0.0.0.0", port=5000)
