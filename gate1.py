import sqlite3
import pandas as pd 


# vamos a cargar la base de datos a Pandas
def cargar_a_dataframe(database_name='miloto.db', table_name='sorteos'):
    try:
        conn = sqlite3.connect(database_name)
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Error al cargar datos desde la base de datos: {e}")
        return None


# Llamada a la función
df = cargar_a_dataframe()
df.set_index('numero_sorteo', inplace=True)
df[['n1', 'n2', 'n3', 'n4', 'n5']] = df['numeros_ganadores'].str.split(',', expand=True)
df.drop(columns=['numeros_ganadores'], inplace=True)
print(df)