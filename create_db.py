import sqlite3

conn = sqlite3.connect('miloto.db')
cursor = conn.cursor()
cursor.execute('''

    CREATE TABLE IF NOT EXISTS sorteos (
               numero_sorteo INTEGER,
               fecha_sorteo DATE,
               numeros_ganadores TEXT
    )
                ''')

conn.close()