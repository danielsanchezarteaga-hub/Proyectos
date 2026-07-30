# imprime los numeros desde n hasta 1 
def imprimir_numeros(n):
    if n < 1:
        return 1
    else: 
        print(n)
        return imprimir_numeros(n - 1)

imprimir_numeros(5)
