import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from from_sql_to_df import cargar_a_dataframe
import warnings

# Load your data
df = cargar_a_dataframe()
df.set_index('numero_sorteo', inplace=True)
df[['n1', 'n2', 'n3', 'n4', 'n5']] = df['numeros_ganadores'].str.split(',', expand=True)

df.drop(columns=['numeros_ganadores'], inplace=True)

# Convert the date to a datetime object and extract useful features
df['fecha_sorteo'] = pd.to_datetime(df['fecha_sorteo'], format='%d-%m-%Y')
df['year'] = df['fecha_sorteo'].dt.year
df['month'] = df['fecha_sorteo'].dt.month
df['day'] = df['fecha_sorteo'].dt.day
df['dayofweek'] = df['fecha_sorteo'].dt.dayofweek

# Drop the original date column as we now have numeric features
df.drop('fecha_sorteo', axis=1, inplace=True)

# Suppress warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names", category=UserWarning)

# Assuming you want to predict each number separately
# Prepare the data for each number prediction
X = df.drop(['n1', 'n2', 'n3', 'n4', 'n5'], axis=1)
y1 = df['n1']
y2 = df['n2']
y3 = df['n3']
y4 = df['n4']
y5 = df['n5']

# Initialize models for each number prediction
model_n1 = RandomForestClassifier(n_estimators=100)
model_n2 = RandomForestClassifier(n_estimators=100)
model_n3 = RandomForestClassifier(n_estimators=100)
model_n4 = RandomForestClassifier(n_estimators=100)
model_n5 = RandomForestClassifier(n_estimators=100)

# Split the data into training and test sets for each number
X_train, X_test, y1_train, y1_test = train_test_split(X, y1, test_size=0.2, random_state=42)
X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size=0.2, random_state=42)
X_train, X_test, y3_train, y3_test = train_test_split(X, y3, test_size=0.2, random_state=42)
X_train, X_test, y4_train, y4_test = train_test_split(X, y4, test_size=0.2, random_state=42)
X_train, X_test, y5_train, y5_test = train_test_split(X, y5, test_size=0.2, random_state=42)

# Train each model
model_n1.fit(X_train, y1_train)
model_n2.fit(X_train, y2_train)
model_n3.fit(X_train, y3_train)
model_n4.fit(X_train, y4_train)
model_n5.fit(X_train, y5_train)

# Make predictions (here you need to provide the features for the next draw)
# For example:
next_draw_features = [[2024, 2, 5, 1]]  # Year: 2024, Month: 2, Day: 5, Day of the week: 1 (Monday)

prediction_n1 = model_n1.predict(next_draw_features)
prediction_n2 = model_n2.predict(next_draw_features)
prediction_n3 = model_n3.predict(next_draw_features)
prediction_n4 = model_n4.predict(next_draw_features)
prediction_n5 = model_n5.predict(next_draw_features)

print(f"Predicted numbers for next draw: {prediction_n1[0]}, {prediction_n2[0]}, \
{prediction_n3[0]}, {prediction_n4[0]}, {prediction_n5[0]} ")