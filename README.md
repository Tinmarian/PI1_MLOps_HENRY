# Sistema de Recomendación con scikit-learn y despliegue de API en Render.

Link al repositorio de GitHub:

  * https://github.com/Tinmarian/PI1_MLOps_HENRY

Link a la API en Render:

  * https://recommendation-system-ycfj.onrender.com/docs#/

Link al video en YT:

 * https://www.youtube.com/watch?v=1Zq2XKiNqBM

En este proyecto se trabajó en un sistema de recomendación de películas mediante una técnica de vectorización sencilla, 
para posteriormente generar el calculo del producto punto con el fin de obtener la distancia del coseno entre la "bolsa de palabras" de cada
película. De esta manera recomendar 5 películas similares bajo nuestro criterio.

Para este proyecto creé este repositorio, el cual cuenta con 5 ramas: main, API_development, EDA, API_deployment y ML_model.

Trabajé la parte de la limpieza de los datos en la rama de main directamente, y a través de las demás ramas, generando merge con la rama main cada que
fue necesario, con excepción de la rama API_deployment, la cual utilicé para conectar a Render y desplegar la API.

El trabajo que se realizo en la limpieza fue principalmente el de separar los datos para poder organizarlos de mejor manera, en la forma de una 
Base de Datos Relacional (aunque realmente nos faltó cargar los datos al RDBMS de PostgreSQL que nos ofrecía Render). Sin embargo, 
se preparó los csv para que funcionaran en una Base de Datos Relacional, utilizando llaves primarias y foráneas. Esto redujo considerablemente el uso
de memoria por archivo, ya que evitamos al máximo las redundancias.

Los archivos resultantes son los siguientes:

  * Archivos de valores únicos:
      * actores.csv
      * directores.csv
      * franquicias.csv
      * generos.csv
      * lenguajes.csv
      * paises.csv
      * productoras.csv
  * Archvivos que conectan los valores únicos (por lo general strings) con las películas correspondientes (PK's and FK's):
      * dir_movies.csv
      * franq_movies.csv
      * gen_movies.csv
      * leng_movies.csv
      * pais_movies.csv
      * pers_movies.csv (actores y pelis)
      * prod_movies.csv

Aplique funciones lambda para modificar valores y como filtros en los dataframes. Utilicé muchos joins todo el tiempo. También realicé "UNION"
mediante pd.concat([]). Utilicé la función eval() para obtener diccionarios de strings. Utilicé bastantes ciclos y mucho control de flujo 
mediante if's. Durante toda la limpieza y el EDA, e incluso en el development y deployment de la API, utilicé solo pandas y os para el 
procesamiento de datos. Fue hasta el modelo de ML que utilicé la librería de scikit-learn.

Para el modelo utilice CountVectorizer() y la cosine_similarity(). Y para no sobrecargar la memoria en Render, cree un archivo nuevo con 
las recomendaciones de cada película:

    * recommended_movies.csv

El cual trabaja con el archivo:

    * movies_model.csv

Para hacer el join necesario y dar las recomendaciones.

Para la "bolsa de palabras" solo utilicé las siguientes columnas: ['title', 'franquicia', 'genero', 'cineastas', 'elenco'].

Además de esta parte principal del proyecto, se realizaron otras 6 funciones que se desplegaron como endpoints en la API. Estas funciones son 
exactamente como las piden en el readme https://github.com/Tinmarian/PI_ML_OPS#readme
