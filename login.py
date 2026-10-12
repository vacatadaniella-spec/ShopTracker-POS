import tkinter as tk
from tkinter import messagebox
from database import connection_db
from products import open_product
from sales import open_sales
from reports import open_reports 

def open_pos():
    pos_window = tk.Toplevel()
    pos_window.title("ShopTracker POS")
    pos_window.geometry("800x500")

    title_label = tk.Label(pos_window, text="Welcome to ShopTracker POS", font=("Arial", 20))
    title_label.pack(pady=30)

    products_button = tk.Button(pos_window, text="Products", width=20, command=open_product)
    products_button.pack(pady=10)

    sales_button = tk.Button(pos_window, text="Sales", width=20, command=open_sales)
    sales_button.pack(pady=10)

    reports_button = tk.Button(pos_window, text="Reports", width=20, command=open_reports)
    reports_button.pack(pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        connection = connection_db()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome to ShopTracker POS")
            open_pos()
        else: 
            messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as error:
        messagebox.showerror("Database Error", str(error))

root = tk.Tk()
root.title("ShopTracker POS Login")
root.geometry("400x300")

username_label = tk.Label(root, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

root.mainloop()

