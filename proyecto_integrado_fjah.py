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

#Verificar duplicados
datafer.duplicated().sum()
duplicados = datafer[datafer.duplicated()]
print(duplicados)

#Nombres - Columna
print(datafer[datafer['name'].isna()])
#Eliminaremos estos datos debido a que tienen muchos datos nulos en toda la fila
datafer.dropna(subset=['name'], inplace=True)

#Year of release
#Tenemos datos nulos, y la columna es un float cuando debería ser un int al tratarse de años
datafer['year_of_release'] = pd.to_numeric(datafer['year_of_release'], errors='coerce').astype('Int64')

#Corregir la columna user score, pasaremos los datos tbd a np.nan y cambiaremos la columna a float
print(datafer['user_score'].unique())
datafer['user_score'].replace('tbd',np.nan,inplace=True)
datafer['user_score'].replace('nan',np.nan,inplace=True)
datafer['user_score'] = pd.to_numeric(datafer['user_score'],errors='coerce')

print(datafer.info())

#verificamos valores de genre
print(datafer['genre'].value_counts())
datafer['genre'] = datafer['genre'].fillna('Other')



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
games_per_year.plot(kind='bar',title='Juegos Lanzados')
plt.show()

#Ingresos de Juegos por plataforma anual
games_per_platform = datafer.groupby(['platform','year_of_release'])['total_sales'].sum()
games_per_platform


##prueba

