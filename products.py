import tkinter as tk
from tkinter import messagebox
from database import connection_db

def open_product():
    root = tk.Toplevel()
    root.title("Product Management")
    root.geometry("400x400")

    def add_product():
        name = name_entry.get()
        category = category_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()

        if not name or not category or not price or not quantity:
            messagebox.showerror("Input Error", "All fields are required")
            return

        try:
            price_value = float(price)
            quantity_value = int(quantity)
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Price must be a number and Quantity must be an integer",
            )
            return

        try:
            connection = connection_db()
            cursor = connection.cursor()

            query = "INSERT INTO products (product_name, category, price, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, category, price_value, quantity_value))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Product added successfully")

            name_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    name_label = tk.Label(root, text="Product Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack()

    category_label = tk.Label(root, text="Category:")
    category_label.pack(pady=5)
    category_entry = tk.Entry(root)
    category_entry.pack()

    price_label = tk.Label(root, text="Price:")
    price_label.pack(pady=5)
    price_entry = tk.Entry(root)
    price_entry.pack()

    quantity_label = tk.Label(root, text="Quantity:")
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    add_button = tk.Button(root, text="Add Product", command=add_product)
    add_button.pack(pady=20)
    

    

    