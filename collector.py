import sqlite3
from miloto_scraper import check_url 

url = 'https://baloto.com/miloto/resultados-miloto/'


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


def check_last_number():
    sql_command = "SELECT MAX(numero_sorteo) FROM sorteos"
    resultado = execute_sql(sql_command)
    return resultado


# get the last lottery session number
sequential = check_last_number()
if sequential[0] == (None,):  # when the database is empty
    last_part = '1'
else:
    last_part = str(sequential+1)  # Get last lottery sequential
url_full = url + last_part
status_code, numero_sorteo, fecha_sorteo, numeros_ganadores = check_url(url_full)
if status_code == 200:
    sql_command = "INSERT INTO sorteos (numero_sorteo, fecha_sorteo, numeros_ganadores) VALUES (?, ?, ?)"
    parameters = (numero_sorteo, fecha_sorteo, ",".join(numeros_ganadores))
    resultados = execute_sql(sql_command, parameters)              
else:
    print(f'Database error: {status_code}')
