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

#Multiplicaremos los valores de user score x10 para que esten a la par de critics
datafer['user_score'] = datafer['user_score'] * 10
print(datafer['user_score'])

print(datafer.info())

#Verificamos la informacion de rating
print(datafer['rating'].unique())

#Agregamos una columna que tenga las ventas totales
#total de ventas
datafer['total_sales'] = datafer['na_sales'] + datafer['eu_sales'] + datafer['jp_sales'] + datafer['other_sales']

#Analisis de Datos
#¿Cuántos juegos fueron lanzados cada año?
#Crearemos una grafica de barra para mostrar el paso del tiempo vs los juegos lanzados
games_per_year = datafer.groupby('year_of_release')['name'].count()
games_per_year.plot(kind='bar',title='Juegos Lanzados', xlabel='Años',ylabel='Cantidad de Juegos Lanzados')
plt.show()

#¿Qué plataformas tienen mayores ventas totales?
#Para esto solo usaremos datos desde el 2010 para ver la evolución de las plataformas
data_since_2010 = datafer[datafer['year_of_release'] >= 2010]
games_per_platform = data_since_2010.groupby(['platform','year_of_release'])['total_sales'].sum().reset_index()
games_per_platform = games_per_platform.pivot(index='year_of_release',columns='platform',values='total_sales')
games_per_platform.plot(kind='bar')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

#El PS4 es una plataforma que ha tenido un creciemiento por encima de otras a traves de los años, despues de esta le siguen Xbox One y Nintendo 3Ds. Es importante resaltar que el PS3 fue la plataforma con más ingresos 2 años antes y el año que salio la PS4

#¿Cómo afectan las reseñas de usuarios/profesionales las ventas?
#Crearemos una columna que nos saque una  reseña global sumando user y critics

datafer['global_score'] = (datafer['user_score'].fillna(0) + datafer['critic_score'].fillna(0))/2

user_score_sales = datafer.groupby('user_score')['total_sales'].sum().reset_index()
user_score_sales.plot(kind='scatter')
plt.show()