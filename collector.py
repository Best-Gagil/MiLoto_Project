import sqlite3
import locale
import os 
from miloto_scraper import check_url 
from datetime import datetime

# Set the locale to Spanish
locale.setlocale(locale.LC_TIME, 'es_ES')

url = 'https://baloto.com/miloto/resultados-miloto/'
database_name = 'miloto.db'


def execute_sql(sql_command, parameters=()):
    """
    sql_command: receive the SQL Command to execute
    parameters: tuple of parameters for the SQL command
    """
    try:
        conn = sqlite3.connect(database_name)
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


# main
if not os.path.exists(database_name):
    print("Database miloto.db doesn't exist. Proceding to create it ...")
    sql_command = ('''

    CREATE TABLE IF NOT EXISTS sorteos (
               numero_sorteo INTEGER,
               fecha_sorteo DATE,
               numeros_ganadores TEXT
    )
                ''')
    resultados = execute_sql(sql_command)

while True:
    # get the last lottery session number
    sequential = check_last_number()
    if sequential[0][0] is None:  # when the database is empty
        last_part = '1'
    else:
        last_part = str(sequential[0][0]+1)  # Get last lottery sequential
    url_full = url + last_part
    status_code, numero_sorteo, fecha_sorteo, numeros_ganadores = check_url(url_full)
    if status_code == 200:
        # Convert the date string to a datetime object
        fecha_sorteo = datetime.strptime(fecha_sorteo, '%d de %B de %Y')
        # Reset the locale to the default value
        locale.setlocale(locale.LC_TIME, None)
        # Format the datetime object to 'DD-MM-YYYY' string
        fecha_sorteo = fecha_sorteo.strftime('%d-%m-%Y')
        sql_command = (
            "INSERT INTO sorteos"
            "(numero_sorteo, fecha_sorteo, numeros_ganadores) "
            "VALUES (?, ?, ?)"
        ) 
        parameters = (numero_sorteo, fecha_sorteo, ",".join(numeros_ganadores))
        resultados = execute_sql(sql_command, parameters)
        print(f'Inserting results sorteo: {numero_sorteo}')
    elif status_code == 500:
        print('No more data to fetch in the URL')         
        break
    else:
        print(f'Connection to URL failed: {status_code}')
        break

