# B5: Run SQL Query
from TaskB.task_b12 import B12
import sqlite3, duckdb

def B5(db_path, query, output_filename):
    if not B12(db_path):
        return None
    
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result