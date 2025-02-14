import os
import sqlite3

def A10():
    db_file = "./data/ticket-sales.db"
    output_file = "./data/ticket-sales-gold.txt"
    
    if not os.path.isfile(db_file):
        raise FileNotFoundError("Database file not found")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
        total_sales = cursor.fetchone()[0] or 0
        conn.close()
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(total_sales))
        
        return "Total sales for Gold tickets computed successfully."
    except Exception as e:
        raise RuntimeError(f"Error computing Gold ticket sales: {e}")