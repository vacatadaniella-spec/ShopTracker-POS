from flask import Flask, render_template 
from database import connection_db
from datetime import date 

app = Flask(__name__)

@app.route("/daily-report")
def daily_report():
    connection = connection_db()
    cursor = connection.cursor(dictionary=True)
    today = date.today()

    query = """SELECT sale_id, user_id, total_amount, sale_date
                FROM sales
                WHERE DATE(sale_date) = %s"""

    cursor.execute(query, (today,))
    sales = cursor.fetchall()

    cursor.close()
    connection.close()

    total_sales = sum(float(sale["total_amount"]) for sale in sales)

    return render_template("Daily_report.html", 
                            sales=sales,
                            total_sales=total_sales,
                            report_date=today)

if __name__ == "__main__":
    app.run(debug=True, port=5001)



