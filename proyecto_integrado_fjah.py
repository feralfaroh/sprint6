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
user_score_sales.plot(kind='scatter', x='user_score', y='total_sales',xlabel='User Score',ylabel='Ventas (Millones)',title='Ventas vs Score')
plt.show()

#Los juegos que tienen un promedio de usuario de 70 a 90 son los que tienen mayores ventas

critic_score_sales = datafer.groupby('critic_score')['total_sales'].sum().reset_index()
critic_score_sales.plot(kind='scatter', x='critic_score', y='total_sales',xlabel='Critic Score',ylabel='Ventas (Millones)',title='Ventas vs Score')
plt.show()

#Los juegos con las calificaciones de los criticos tienen un comportamiento similar al de user score

#Ahora queremos saber cuales son los generos mas rentables, para esto usaremos datos apartir del 2010 para que los datos sean más precisos a la hora de tomar una decision
#¿Qué géneros son más rentables?

sales_per_genre = data_since_2010.groupby('genre')['total_sales'].sum().reset_index()
sales_per_genre
sales_per_genre.plot(kind='bar',x='genre',y='total_sales')
plt.suptitle('Ventas por genero de juego', fontsize=15)
plt.title('Datos de 2010 a 2016', fontsize=10)
plt.xticks(rotation= 35)
plt.show()

#Evolucion temporal
sales_per_genre_yearly = data_since_2010.groupby(['genre','year_of_release'])['total_sales'].sum().reset_index()
sales_per_genre_yearly = sales_per_genre_yearly.pivot(index='year_of_release',columns='genre',values='total_sales')
sales_per_genre_yearly.plot()
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()

#Creacion de perfiles 
#Identifica las cinco plataformas y géneros principales.
#Analiza cómo afecta la clasificación ESRB a las ventas.

#Perfil de norteamerica (NA)
#plataforma
na_profile_platform = datafer.groupby('platform')['na_sales'].sum().reset_index()
na_profile_platform = na_profile_platform.sort_values(by='na_sales', ascending=False)
print(f"Los plataformas que tienen más ventas en Norteamerica son: {na_profile_platform.head(5)}")
#generos
na_profile_genre = datafer.groupby('genre')['na_sales'].sum().reset_index()
na_profile_genre = na_profile_genre.sort_values(by='na_sales', ascending=False)
print(f"Los generos que tienen más ventas en Norteamerica son: {na_profile_genre.head(5)}")

#Perfil de Union Europea (UE)
#plataforma
na_profile_platform = datafer.groupby('platform')['eu_sales'].sum().reset_index()
na_profile_platform = na_profile_platform.sort_values(by='eu_sales', ascending=False)
print(f"Los plataformas que tienen más ventas en Union Europea son: {na_profile_platform.head(5)}")
#generos
na_profile_genre = datafer.groupby('genre')['eu_sales'].sum().reset_index()
na_profile_genre = na_profile_genre.sort_values(by='eu_sales', ascending=False)
print(f"Los generos que tienen más ventas en Union Europea son: {na_profile_genre.head(5)}")

#Perfil de Japon (jp)
#plataforma
jp_profile_platform = datafer.groupby('platform')['jp_sales'].sum().reset_index()
jp_profile_platform = jp_profile_platform.sort_values(by='jp_sales', ascending=False)
print(f"Los plataformas que tienen más ventas en Japon son: {na_profile_platform.head(5)}")
#generos
jp_profile_genre = datafer.groupby('genre')['jp_sales'].sum().reset_index()
jp_profile_genre = jp_profile_genre.sort_values(by='jp_sales', ascending=False)
print(f"Los generos que tienen más ventas en Japon son: {na_profile_genre.head(5)}")

#Prueba hipótesis
#Prueba las siguientes:
#Las calificaciones promedio de usuarios para Xbox One y PC son iguales.


#Las calificaciones promedio para los géneros de Acción y Deportes son diferentes.


