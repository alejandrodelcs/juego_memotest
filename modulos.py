from time import time
from random import randint, randrange
from random import shuffle
from tkinter import Button


MAX_INGRESO = 2
FACIL = 2
MEDIO = 4
DIFICIL = 8


"""
    PRE    Recibe la el tamaño de la lista de fichas.
    POST:  Devueve la abscisa (eje x), la fila debe tener max 4 posiciones,
           si es menor a esa cantidad x=1 por condicion de enunciado
           caso contrario y>0
    Alejandro Del Carpio Sanchez
"""
def validacionAbscisa(dimension):
    posX = 0 #El enunciado pide que empiece desde esa posición 
    if dimension > 4:
        posX = randint(0, (dimension//4)-1)
    return posX



"""
    PRE:   Recibe la el tamaño de la lista de fichas.
    POST:  Devueve la ordenada (eje y), la fila debe tener max 4 posiciones,
           si es superior a esa cantidad devuelve un entero comprendido
           entre 1 y la dimension dividido al número de max de posiciones,
           caso contrario un rango entre 1 y max posiciones (4)
            
    Alejandro Del Carpio Sanchez
"""
def validacionOrdenada(dimension):
    posY = randint(0, dimension-1)
    if dimension > 4:
        posY = randint(0, 3)
    return posY


"""
    PRE:  Recibe el diccionario en plena construcción, una lista de
        enteros de tamaño 2 y el tamaño de la lista de fichas
    POST: Devuelve una lista de enteros de tamaño 2 que no este repetida
        en el diccionario .
    Alejandro Del Carpio Sanchez
"""
def validarCoordenada(diccTablero, coordenada, dimension):

    listaDePosiciones = [y for x in diccTablero.values() for y in x]
    existePosicion = coordenada in listaDePosiciones
    while existePosicion:
        posX = validacionAbscisa(dimension)
        posY = validacionOrdenada(dimension)
        coordenada = [posX, posY]
        existePosicion = coordenada in listaDePosiciones
    return coordenada


"""
    PRE:  Recibe la lista de fichas de tamaño N y su tamaño .
    POST: Devuelve un diccionario donde las claves son las fichas
            y su valor representa las posiciones en el tablero.
    Alejandro Del Carpio Sanchez
"""
def crearPosiciones(nivel):
    diccTablero = {}    
    listaFichas = crearFichas(nivel)
    dimension = len(listaFichas)
    for ficha in listaFichas:
        posX = validacionAbscisa(dimension)
        posY = validacionOrdenada(dimension)
        if ficha in diccTablero:
            coordenada = validarCoordenada(
                diccTablero, [posX, posY], dimension)
            diccTablero[ficha].append(coordenada)
        else:
            coordenada = validarCoordenada(
                diccTablero, [posX, posY], dimension)
            diccTablero[ficha] = [coordenada]
    return diccTablero



"""
    PRE: Recibe el nivel del juego. 
    POST: Segun el nivel de dificultad, devuelve de forma al azar
          las fichas de forma aleatoria, en un sistema de mayusculas-minusculas.
    Leandro.A.Peñaloza
"""
def crearFichas(nivel):

    letras = []
    letraMayuscula = randrange(65,82,2)
    letraMinuscula = randrange(98,114,2)

    for i in range(0, nivel, 2):
        letra = chr(letraMayuscula + i)
        letras.append(letra)
        letra_dos = chr(letraMinuscula + i)
        letras.append(letra_dos)
        
    letras = letras * 2
    shuffle(letras)
    return letras

"""
    PRE: Recibe un entero que representa el nivel del juego
    POST: Devuelve una listas de listas con un caracter ya cargado
    Andres Doskoch
"""
def crearTablero(nivel):
    if nivel > 0:
        matriz = []
        for i in range(nivel//2):
            matriz.append([])
            for j in range(1, 5):
                matriz[i].append('?')
    return matriz



"""
    PRE:  Recibe una lista con letra y coordenada, ademas recibe un diccionario con las posiciones
          del tablero y una lista con fichas encontradas
          ListaPareja-->[[letra1,coordenada1],[letra2,coordenada2]]
    POST: Retorna un numero, si encontro la letra devuelve 1 caso contrario 0
     Alejandro Del Carpio / Leandro.A.Peñaloza / Agustin Allelo    
"""
def validarIngresoPosicion(listaPareja, diccTablero):
    punto = 0
    if listaPareja[0][0] == listaPareja[1][0]:
        punto = 1
        del(diccTablero[listaPareja[0][0]])  
    return punto



def comprobarLetra(diccTablero,coordenada):
    encontrado = 0
    pos = 0
    infoUsuario = []

    tuplaPosiciones = list(diccTablero.items())
    while pos < len(tuplaPosiciones) and encontrado < 2: 
        if coordenada[0] in tuplaPosiciones[pos][1]:
            encontrado += 1
            infoUsuario.append([tuplaPosiciones[pos][0], coordenada[0]])
        if coordenada[1] in tuplaPosiciones[pos][1]:
            encontrado += 1
            infoUsuario.append([tuplaPosiciones[pos][0], coordenada[1]]) 
        pos += 1
    return validarIngresoPosicion(infoUsuario,diccTablero)


def crearDiccionario(listaUsuarios):
    dicc = {}
    
    for usuario in listaUsuarios:
        dicc[usuario] = [0,0,0]

    return dicc

        


