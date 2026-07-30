def sumar_digitos(n):

    if n < 10:
        return n
    else:
        return n % 10 + sumar_digitos(n // 10)


def facto(n):

    if n == 0 or n == 1:
        return 1
    else:
        return n * facto(n - 1)


def menu():

    numero = int(input("Digite un numero: "))

    suma = sumar_digitos(numero)

    resultado = facto(suma)

    print("La suma de los digitos es:", suma)
    print("El factorial es:", resultado)


menu()