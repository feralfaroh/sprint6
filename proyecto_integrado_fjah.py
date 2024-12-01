import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

datafer = pd.read_csv('games.csv')
print(datafer.head(10))

#Limpiar datos
print(datafer.info())
print(datafer.value_counts())
#Corregir nombre de columnas
new_names = []
for col in datafer.columns:
    new_names.append(col.lower())
datafer.columns = new_names

datafer.duplicated().sum()

#Corregir tipo de datos en las columnas
#corregiremos la columna de year debido a que es el release year
datafer['year_of_release'] = datafer['year_of_release'].fillna(0).astype(int)

#verificamos valores de genre
print(datafer['genre'].value_counts())
datafer['genre'] = datafer['genre'].fillna('Other')

#rellenamos valores Nan de 'name'
datafer['name'] = datafer['name'].fillna('Name Unavailable')


#Verifocar valores de critic score
print(datafer['critic_score'].unique())
#transformar datos
datafer['critic_score'] = datafer['critic_score'].replace('nan', np.nan)
datafer['critic_score'] = datafer['critic_score'].astype(float)

#verificar valores user score
print(datafer['user_score'].unique())
#transformar datos
datafer['user_score'] = datafer['user_score'].replace('nan', np.nan)


#Convertimos los valores a float incluyendo tbd debido a que no sabremos que calificacion pondriz el usuario
datafer['user_score'] = pd.to_numeric(datafer['user_score'], errors='coerce')
calif = datafer.groupby('name')['user_score'].unique()
calif

#total de ventas

datafer['total_sales'] = datafer['na_sales'] + datafer['eu_sales'] + datafer['jp_sales'] + datafer['other_sales']

#Juegos por anio
games_per_year = datafer.groupby('year_of_release')['name'].count()
games_per_year.plot(kind='bar')
plt.show()

##prueba

