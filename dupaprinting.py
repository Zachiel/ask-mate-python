import psycopg2
import psycopg2.extras

# dict_cur.execute("SELECT * FROM answer")
# rec = dict_cur.fetchall()
# dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

conn = psycopg2.connect("dbname=cc_ask_mate user=cc_ask_mate password=test123")
cur = conn.cursor()
cur.execute("SELECT * FROM answer;")
desc = cur.description
column_names = [col[0] for col in desc]
data = [dict(zip(column_names, row))  
        for row in cur.fetchall()]
print((data))
conn.close()