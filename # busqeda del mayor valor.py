# busqeda del mayor valor
def encontrar_mayor(lista_numeros):
    if lista_numeros == []:
        return "La lista está vacía."
    mayor_actual = lista_numeros[0]

    for numero in lista_numeros:
        if numero > mayor_actual:
            mayor_actual = numero

    return mayor_actual
