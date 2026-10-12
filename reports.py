import tkinter as tk
from tkinter import messagebox
from database import connection_db 

def open_reports():
    root = tk.Toplevel()
    root.title("ShopTracker POS - Reports")
    root.geometry("600x500")

    title_label = tk.Label(root, text="ShopTracker POS - Reports", font=("Arial", 20))
    title_label.pack(pady=20)

    def daily_sales_report():
        try:
            connection = connection_db()
            cursor = connection.cursor()

            query = """SELECT sale_id, sale_date, total_amount
                        FROM sales
                        WHERE DATE(sale_date) = CURRENT_DATE()
                        ORDER BY sale_date DESC
                """
            cursor.execute(query)
            sales = cursor.fetchall()

            cursor.close()
            connection.close()

            if not sales:
                messagebox.showinfo("Daily sales report",
                                    "No sales have been recorded today")
                return

            report_window = tk.Toplevel(root)
            report_window.title("Daily sales report")
            report_window.geometry("600x400")

            heading = tk.Label(report_window,
                               text="Daily sales report",
                               font=("Arial", 18))
            heading.pack(pady=15)

            report_text = tk.Text(report_window,
                                  width=70,
                                  height=18)
            report_text.pack(padx=10, pady=10)
            total = 0

            report_text.insert(tk.END,
                               "Sale ID        Date & Time     Amount\n")
            report_text.insert(tk.END, "-" * 55 + "\n")

            for sale in sales:
                sale_id, sale_date, amount = sale
                total += float(amount)
                report_text.insert(tk.END,
                                   f"{sale_id:<14}{sale_date}       R{float(amount):.2f}\n")

            report_text.insert(tk.END, "\n")
            report_text.insert(tk.END, f"Total Sales: R{total:.2f}")
            report_text.config(state=tk.DISABLED)

        except Exception as error:
            messagebox.showerror("Report error", str(error))

    def sales_history_report():
        try:
            connection = connection_db()
            cursor = connection.cursor()

            query = """SELECT sale_id, sale_date, total_amount
                        FROM sales
                        ORDER BY sale_date DESC
                    """
            cursor.execute(query)
            sales = cursor.fetchall()
            cursor.close()
            connection.close()

            if not sales:
                messagebox.showinfo("Sales history report",
                                     "No sales have been recorded yet")
                return

            report_window = tk.Toplevel(root)
            report_window.title("Sales history report")
            report_window.geometry("700x400")

            heading = tk.Label(report_window,
                               text="Sales history report",
                               font=("Arial", 18))

            heading.pack(pady=15)

            report_text = tk.Text(report_window,
                                  width=80,
                                  height=18)
            report_text.pack(padx=10, pady=10)
            total = 0

            report_text.insert(tk.END,
                               "Sale ID        Date & Time     Amount\n")

            report_text.insert(tk.END, "-" * 65 + "\n")

            for sale in sales:
                sale_id, sale_date, amoount = sale
                total += float(amoount)

                report_text.insert(tk.END,
                                   f"{sale_id:<15}{sale_date}    R{float(amoount):.2f}\n")

                report_text.insert(tk.END, "\n")
            report_text.insert(tk.END, f"Total Sales: R{total:.2f}")

            report_text.config(state=tk.DISABLED)

        except Exception as error:
            messagebox.showerror("Report error", str(error))

    daily_report_button = tk.Button(root, text="Daily sales report",
                                    width=26,
                                    command=daily_sales_report)

    daily_report_button.pack(pady=20)
                
    history_report_button = tk.Button(root, text="Sales history report",
                                        width=26,
                                        command=sales_history_report)
    history_report_button.pack(pady=10)