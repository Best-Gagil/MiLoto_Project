import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from from_sql_to_df import cargar_a_dataframe

# Cargamos los datos de sorteos históricos
df = cargar_a_dataframe()
df.set_index('numero_sorteo', inplace=True)

# Convertir la columna de números ganadores en una lista de números
df['numeros_ganadores'] = df['numeros_ganadores'].apply(lambda x: [int(n) for n in x.split(',')])


# Crear una serie temporal con los números ganadores
time_series = pd.Series([number for numbers in df['numeros_ganadores'] for number in numbers])

# Entrenar un modelo ARIMA para predecir los próximos números ganadores
model = ARIMA(time_series, order=(5,1,0))  # Especificar el orden del modelo ARIMA
model_fit = model.fit()

# Realizar una predicción para los próximos números ganadores
forecast = model_fit.forecast(steps=5)  # Predecir 5 números para el próximo sorteo

# Redondear las predicciones y asegurarse de que estén en el rango del sorteo (1-39)
rounded_forecast = forecast.round().astype(int)
rounded_forecast = rounded_forecast.clip(lower=1, upper=39)

# Imprimir los números predichos para el próximo sorteo
print("Números predichos para el próximo sorteo:\n", rounded_forecast)

