import random
import numpy as np
from Modulos.Utils import Truncate

'''
Funcion que por detras corre una distribucion uniforme.
'''
def ListaAleatoriaNativa(n, inferior, superior, s=None):
    if superior == 1:
        superior = 1.0001
    if s != 0:
        random.seed(s)
    #La funcion aleatoria se parametriza con el rango [0, 1.00001] para generar numeros aleatorios menores o iguales a uno
    #por algunos decimales, que luego son truncados mediante la funcion
    numbers_array = list([Truncate(random.uniform(inferior,superior), 4) for i in range(n)])
    return numbers_array

'''La función genera una muestra de n números aleatorios con distribución exponencial negativa
    Parametros: n: tamaño de la muestra, media: valor de la media
    Si se ingresa un lambda negativo la funcion genera números comprendidos entre infinito negativo y cero. 
    Si se ingresa un lambda positivo la funcion genera números que se encuentran entre cero e infinito
    Retorna list : Lista con los números generados
'''
def distribucionExponencial(n, media):
    valor_lambda = 1 / media
    return list([Truncate(random.expovariate(valor_lambda), 4) for i in range(n)])

'''La función genera una lista de n números aleatorios con distribución normal usando el método de Box-Muller
    Parámetros: n: tamaño de la muestra, mu: media, sigma: desviación estándar
    Retorna list: lista con los números generados
'''
def distribucionNormal(n, mu, sigma):
    return list([Truncate(random.gauss(mu, sigma),4) for i in range(n)])

