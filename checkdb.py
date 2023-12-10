import sqlite3

def execute_sql(sql_command, parameters=()):
    """
    sql_command: receive the SQL Command to execute
    parameters: tuple of parameters for the SQL command
    """
    try:
        conn = sqlite3.connect('miloto.db')
        cursor = conn.cursor()
        
        # Execute the SQL command alone or with parameters
        cursor.execute(sql_command, parameters)
        
        # Fetch results if any
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.commit()  # Don't forget to commit changes
        conn.close()
    except sqlite3.Error as e:
        print(f"The SQLite error reads: {e}")
        resultados = None  # Handle the case where an error occurs
    return resultados

""" probamos meter un dato en la base de datos
numero_sorteo = 1
fecha_sorteo = '20-01-2020'
numeros_ganadores = ['1', '2', '3', '4', '5']

sql_command = "INSERT INTO sorteos (numero_sorteo, fecha_sorteo, numeros_ganadores) VALUES (?, ?, ?)"
parameters = (numero_sorteo, fecha_sorteo, ",".join(numeros_ganadores))

print(execute_sql(sql_command, parameters))
"""
sql_command = "SELECT * FROM sorteos"
print(execute_sql(sql_command))
