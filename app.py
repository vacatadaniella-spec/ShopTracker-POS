import tkinter as tk
from products import open_product
from sales import open_sales
from reports import open_reports 

def open_pos():
    root = tk.Tk()
    root.title("ShopTracker POS")
    root.geometry("800x500")

    title_label = tk.Label(root, text="Welcome to ShopTracker POS", font=("Arial", 20))
    title_label.pack(pady=30)

    products_button = tk.Button(root, text = "Products", width=20, command=open_product)
    products_button.pack(pady=10)

    sales_button = tk.Button(root,text = "Sales", width=20, command=open_sales)
    sales_button.pack(pady=10)

    reports_button = tk.Button(root, text = "Reports", width=20, command=open_reports)
    reports_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_pos()