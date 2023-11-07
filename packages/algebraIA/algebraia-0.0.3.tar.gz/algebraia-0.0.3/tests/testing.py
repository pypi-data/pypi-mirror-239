import sys


sys.path.append('/Users/fernandoleonfranco/Documents/GitHub/LibreriaAlgebra/LibreriaAlgebra/src')

from algebraIA import archivoTest as al #type: ignore 

matrizA,matrizB,matrizC = al.matriz(2,2,2,2)

def impresoraMatriz(matriz):
    for renglon,lista in enumerate(matriz):
        renglonLista = []
        columnas = matriz[renglon]
        for columna in columnas:
            renglonLista.append(columna)
        print(renglonLista)


print(f"Matriz a:")
impresoraMatriz(matrizA)

print(f"Matriz b:")
impresoraMatriz(matrizB)

print(f"Matriz c:")
impresoraMatriz(matrizC)