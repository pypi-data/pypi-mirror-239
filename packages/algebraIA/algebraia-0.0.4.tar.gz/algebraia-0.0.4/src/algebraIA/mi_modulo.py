import __init__ as al

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



# Listas o vectores aleatorios
listaUno = [-10,55,23]
listaDos = [10,-55,-23]
listaTres = [5,5,5]
listaCuatro = [1,1,1]
listaCinco = [2,2,1]


resultado = al.vectorRestultante(listaUno,listaDos,listaTres,listaCuatro,listaCinco)
print(f" Resultado de la suma del vector: {resultado}")