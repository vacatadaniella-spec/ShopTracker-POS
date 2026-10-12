from flask import Flask, jsonify
from database import connection_db 

app = Flask(__name__)
@app.route("/api/products", methods=["GET"])
def get_products():
    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(products)

@app.route("/api/stock", methods=["GET"])
def get_stock():
    connection = connection_db()
    cursor = connection.cursor()

    cursor.execute(""" SELECT product_id, product_name, category, quantity 
                    FROM products""")

    stock = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(stock)

if __name__ == "__main__":
    app.run(debug=True, port=5001)