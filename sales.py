import tkinter as tk
from tkinter import messagebox
import webbrowser
from database import connection_db

def open_sales():
    root = tk.Toplevel()
    root.title("Sales Management")
    root.geometry("600x650")

    title_label = tk.Label(root, text="ShopTracker POS - Sales Management", font=("Arial", 20))
    title_label.pack(pady=20)

    product_label = tk.Label(root, text="Product ID:")
    product_label.pack()
    product_entry = tk.Entry(root)
    product_entry.pack()

    quantity_label = tk.Label(root, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    cart_label = tk.Label(root, text="Cart:", font=("Arial", 14))
    cart_label.pack(pady=15)

    cart_listbox = tk.Listbox(root, width=60, height=10)
    cart_listbox.pack()

    total_label = tk.Label(root, text="Total: R0.00", font=("Arial", 14))
    total_label.pack(pady=15)

    cart = []
    total = 0

    def add_to_cart():
        nonlocal total

        product_id = product_entry.get()
        quantity = quantity_entry.get()

        if not product_id or not quantity:
            messagebox.showerror("Input Error", "Both Product ID and Quantity are required")
            return

        try:
            quantity_value = int(quantity)
            product_id = int(product_id)

            if quantity_value <= 0:
                raise ValueError

        except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a positive integer")
                return

        connection = connection_db()
        cursor = connection.cursor()

        query = "SELECT product_name, price, quantity FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        cursor.close()
        connection.close()

        if not product:
            messagebox.showerror("Product Not Found", "No product found with the given Product ID")
            return

        product_name, price, stock = product

        if quantity_value > stock:
            messagebox.showerror("Stock Error", "Not enough stock available")
            return

        subtotal = price * quantity_value

        cart.append({
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity_value,
            "unit_price": price,
            "subtotal": subtotal
        })

        total += subtotal
        cart_listbox.insert(tk.END,
                         f"{product_name} x {quantity_value} - R{subtotal:.2f}")

        total_label.config(text=f"Total: R{total:.2f}")

        product_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

    def generate_receipt(sale_id):
        receipt_file = f"receipt_{sale_id}.html"

        html = f"""
        <html>
        <head>
            <title>Receipt - Sale ID {sale_id}</title>
        </head>
        <body>
            <h1>ShopTracker POS - Receipt</h1>
            <h2>Sales Receipt</h2>
            <p><strong>Sale ID:</strong> {sale_id}</p>

            <hr>
            <table border="1" cellpadding="5" cellspacing="8">

                <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Unit Price</th>
                    <th>Subtotal</th>
                </tr>
        """
        for item in cart:
            html += f"""
                <tr>
                    <td>{item['product_name']}</td>
                    <td>{item['quantity']}</td>
                    <td>R{float(item['unit_price']):.2f}</td>
                    <td>R{float(item['subtotal']):.2f}</td>
                </tr>
        """
        html += """
            </table>
            <h3>Total: R{:.2f}</h3>
            <p>Thank you for sharing with ShopTracker POS.</p>
        </body>
        </html>
        """

        with open(receipt_file, "w" , encoding="utf-8") as file:
            file.write(html)

        webbrowser.open(receipt_file)


    def process_sale():
        if not cart:
            messagebox.showerror("Cart Empty", "No items in the cart to process")
            return

        try:
            connection = connection_db()
            cursor = connection.cursor()

            sale_query = """INSERT INTO sales (sale_id, user_id, sale_date, total_amount)
            VALUES (NULL, %s, CURRENT_TIMESTAMP, %s)"""

            cursor.execute(sale_query, (1, total))
            sale_id = cursor.lastrowid

            for item in cart:
                item_query = """INSERT INTO sales_items (sale_id, product_id, unit_price, subtotal)
                VALUES (%s, %s, %s, %s)"""

                cursor.execute(
                    item_query,
                    (
                        sale_id,
                        item["product_id"],
                        item["unit_price"],
                        item["subtotal"],
                    ),
                )

                stock_query = """
                    UPDATE products
                    SET quantity = quantity - %s
                    WHERE product_id = %s
                """

                cursor.execute(
                    stock_query,
                    (item["quantity"], item["product_id"]),
                )

            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo(
                "Sale Processed",
                f"Sale processed successfully.\nTotal: R{total:.2f}",
            )

            generate_receipt(sale_id)

        except Exception as error:
            messagebox.showerror("Sale Error", str(error))

    add_button = tk.Button(root, text="Add to Cart", command=add_to_cart)
    add_button.pack(pady=10)

    process_sale_button = tk.Button(root, text="Process Sale", command=process_sale)
    process_sale_button.pack(pady=10)

