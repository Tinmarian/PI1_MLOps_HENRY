import pandas as pd 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def saludo():
    return {"Hello":"World"}

@app.get("/idioma/{idioma}")
def peliculas_idioma(idioma:str):
    idioma = idioma.lower()
    df = pd.read_csv('clean_data/movies.csv')
    dfx = pd.read_csv('clean_data/lenguajes.csv')
    dfy = pd.read_csv('clean_data/leng_movies.csv')
    df = df[df.original_language == idioma]
    df = df.merge(dfy,how='left')
    df = df.merge(dfx,how='left')
    abrev = idioma
    idioma = df.lenguaje[0]
    return {"La cantidad de películas producidas originalmente en":f"{idioma} ({abrev})", "son": f"{len(df)}"}

@app.get("/pelicula/{pelicula}")
def peliculas_duración(pelicula:str):
    pelicula = pelicula.title()
    df = pd.read_csv('clean_data/movies.csv')
    row = df[df.title == pelicula]
    duracion = row.runtime.item()
    anio = row.release_year.item()
    return {"La pelicula" : f"{pelicula}", "tiene una duración de" : f"{duracion} minutos", "Año": f"{anio}"}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia:str):
    franquicia = franquicia.title()
    df = pd.read_csv('clean_data/franquicias.csv')
    dfx = pd.read_csv('clean_data/franq_movies.csv')
    dfy = pd.read_csv('clean_data/movies.csv')
    df = df[df.franquicia == franquicia]
    df = df.merge(dfx)[['id_peli','franquicia']]
    df = df.merge(dfy)[['title','franquicia','revenue','budget']]
    df['ganancia'] = df.revenue - df.budget
    g_total = df.ganancia.sum()
    g_promedio = df.ganancia.mean()
    peliculas = len(df)
    return {"La franquicia" : f"{franquicia}", "tiene un total de" : f"{peliculas} peliculas", "una ganancia total de" : f"{g_total}", "y una ganancia promedio de" : f"{g_promedio}"}

@app.get("/pais/{pais}")
def peliculas_pais(pais:str):
    pais = pais.title()
    df = pd.read_csv('clean_data/paises.csv')
    dfx = pd.read_csv('clean_data/pais_movies.csv')
    df = df.merge(dfx,how='right')
    peliculas = len(df[df.pais == pais])
    return {"Se producieron" : f"{peliculas} peliculas", "en el pais" : f"{pais}"}

@app.get("/productora/{productora}")
def productoras_exitosas(productora:str):
    productora = productora.title()
    df = pd.read_csv('clean_data/productoras.csv')
    dfx = pd.read_csv('clean_data/prod_movies.csv')
    dfy = pd.read_csv('clean_data/movies.csv')
    df = df[df.productora == productora]
    df = df.merge(dfx)[['id_peli','productora']]
    df = df.merge(dfy)[['productora','revenue']]
    peliculas = len(df)
    rev_total = df.revenue.sum()
    return {"La productora" : f"{productora}", f"tiene {peliculas} peliculas" : f"con un revenue total de {rev_total} entre todas"}

@app.get("/director/{director}")
def get_director(director:str):
    director = director.title()
    df = pd.read_csv('clean_data/directores.csv')
    dfx = pd.read_csv('clean_data/dir_movies.csv')
    dfy = pd.read_csv('clean_data/movies.csv')
    df = df[df.director == director]
    df = df.merge(dfx)[['id_peli','director']]
    df = df.merge(dfy)[['title','release_date','revenue','budget','return']]
    retorno = df.revenue.sum()/df.budget.sum()
    listas = df.to_numpy().tolist()
    return {f"El director {director}" : f"tiene un éxito medido a través del retorno de todas sus películas de {retorno}.", "Las películas que dirigió son:" : f"{listas}", "La ecuación que se utilizó para obtener el retorno es:" : "df.revenue.sum()/df.budget.sum(), donde 'df' es el dataframe filtrado por el director seleccionado."}

@app.get("/recomendacion/{pelicula}")
def recomendacion(pelicula):
# The `try` block is used to handle exceptions or errors that may occur during the execution of the
# code. In this case, the code is trying to convert the `pelicula` variable to an integer using the
# `int()` function. If the conversion is successful, it means that `pelicula` is an integer and the
# code continues executing normally. However, if the conversion raises a `ValueError` (i.e.,
# `pelicula` is not a valid integer), the code jumps to the `except` block to handle the exception.
    try:
        pelicula = int(pelicula)
    except ValueError:
        pass
    df = pd.read_csv('clean_data/movies_model.csv')
    dfx = pd.read_csv('clean_data/recommended_movies.csv')
    if type(pelicula) == str:
        pelicula = pelicula.title()
        lista = list(dfx[dfx.title == pelicula].idx_recommend)
    elif type(pelicula) == int:
        lista = list(dfx[dfx.id_peli == pelicula].idx_recommend)
        pelicula = dfx.title[dfx.id_peli == pelicula][:1].item()
    else:
        return {"Debes introducir un valor entero (int) que pertenezca al id de alguna película" : "O el nombre de una película en inglés (str)"}

    recomendacion = df.loc[lista][['id_peli', 'title']]
    recomendacion.columns = ['id_peli','recomendaciones']
    dfy = pd.read_csv('clean_data/movies_dataset.csv')

    if not recomendacion.empty:
        return {
            "Ingresaste la película: ": f"{pelicula}",
            "Las recomendaciones son: ": f"1.- [{recomendacion.recomendaciones[:1].item()}]; 2.- [{recomendacion.recomendaciones[1:2].item()}]; 3.- [{recomendacion.recomendaciones[2:3].item()}]; 4.- [{recomendacion.recomendaciones[3:4].item()}]; 5.- [{recomendacion.recomendaciones[4:5].item()}]",
        }
    else: 
        return {
            "Dentro del dataset no se encuentra la película: " : f"{pelicula}", 
            "Recuerda que, debido a los procesos de limpieza y preprocesamiento, solo contamos con: " : f"{len(df)} películas", 
            "de un total de: " : f"{len(dfy)} películas."}