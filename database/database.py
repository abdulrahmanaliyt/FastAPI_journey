import sqlite3
import sys
from builtins import input, int, len

from rich import print

# 1. Connect to the database (It creates if it doesn't exist) and store the connection in a products.db file 
conn = sqlite3.connect("products.db")

# 2. Create a cursor object to execute SQL commands
cursor = conn.cursor()

# 3. Create a table to store product information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        Stock INTEGER NOT NULL,
        Status TEXT NOT NULL
    )
''')

# Insert some sample data into the products table
# cursor.execute('''
#     INSERT INTO products (id, name, price, Stock, Status)
#     VALUES
#         (1, 'Product A', 10.99, 100, 'Available'),
#         (2, 'Product B', 15.49, 50, 'Available'),
#         (3, 'Product C', 7.99, 200, 'Out of Stock')
# ''')

# update the price of a product with id 1
# cursor.execute('''
#     UPDATE products
#     SET price = 12.99
#     WHERE id = 1
# ''')

# We don't use f string due to SQL injection vulnerability, instead we use parameterized queries to prevent SQL injection attacks.

# # Update the stock value of the product with the given id
# # Order matters here in this 

new_stock = int(input("Enter the new stock value: "))  # Converted to int to match database type
product_id = int(input("Enter the product id to update: "))  # Converted to int to match database type

# Name place holders are used in the SQL query to prevent SQL injection attacks. The values for these placeholders are provided as a tuple in the second argument of the execute() method.

# cursor.execute('''
#     UPDATE products
#     SET Stock = ?
#     WHERE id = ?
# ''', (new_stock, product_id))

# To intert vlaue if oreder not matter in SQL, you can use the following code snippet:

# postinal placeholders are used in the SQL query to prevent SQL injection attacks. The values for these placeholders are provided as a dictionary in the second argument of the execute() method.

cursor.execute('''
    UPDATE products
    SET Stock = :new_stock
    WHERE id = :product_id
''', {"new_stock": new_stock, "product_id": product_id})

# # delete a product with id 2
# # Order matters in SQL, so make sure to execute the delete statement after the update statement if you want to see the updated stock value before deletion.
# cursor.execute('''    
#     DELETE FROM products
#     WHERE id = 2
# ''')



# Select all rows from the products table and print them
cursor.execute('SELECT * FROM products')

# Fetch all rows from the executed query
# rows = cursor.fetchall()

# Fetch only the first 5 rows from the executed query
# rows = cursor.fetchmany(5)

# rows = cursor.fetchmany(1)  # Fetch only the first row from the executed query

# 4. Print the rows to verify the data
# print("Products in the database:\n", rows)
# print("Number of rows fetched:", len(rows))

print("Number of rows in the products table:", cursor.rowcount)  # This will return -1 for SELECT statements
# 4. Commit the changes and close the connection
conn.commit()

# Drop the products table if needed
# cursor.execute('DROP TABLE products')

# 5. Now close the connection to the database when done
conn.close()

# # 5. Function to add a new product to the database
# def add_product(name, price, stock, status):