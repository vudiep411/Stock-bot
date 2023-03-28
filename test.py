import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


id = 'vudiep'
cur.execute("SELECT * FROM trader WHERE id=%s;", (id,))

result = cur.fetchone()

if not result:
    print('No Res')
else:
    print(result)


conn.commit()
cur.close()
conn.close()